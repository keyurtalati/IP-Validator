from shodan import Shodan
import shodan
from progress.bar import Bar
from prettytable.colortable import ColorTable, Themes
from censys.search import CensysHosts
from termcolor import colored,cprint
from nslookup import Nslookup
api = Shodan('Shodan-API-key')
table1 = ColorTable(['Number','IP Address','Result','Source'],theme=Themes.OCEAN)
table1.align["Line"] = "l"
input_file=open("ips.txt","r")
valid_dns_ip=[]
list_of_input_domain=[]

print("\n██╗██████╗     ██╗   ██╗ █████╗ ██╗     ██╗██████╗  █████╗ ████████╗ ██████╗ ██████╗")
print("██║██╔══██╗    ██║   ██║██╔══██╗██║     ██║██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗")
print("██║██████╔╝    ██║   ██║███████║██║     ██║██║  ██║███████║   ██║   ██║   ██║██████╔╝")
print("██║██╔═══╝     ╚██╗ ██╔╝██╔══██║██║     ██║██║  ██║██╔══██║   ██║   ██║   ██║██╔══██╗")
print("██║██║          ╚████╔╝ ██║  ██║███████╗██║██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║")
print("╚═╝╚═╝           ╚═══╝  ╚═╝  ╚═╝╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝")
print(colored("\t\t\t\t - Author : Keyur Talati | Release Date : 19 Nov 2022\n","yellow"))                                                                                   

with open(r'domain_for_dns.txt', 'r',encoding="utf8") as fp:
            lines = fp.readlines()
            for domain in lines:
                domain=domain.replace("\n", "")
                list_of_input_domain.append(domain)
                dns_query = Nslookup()
                dns_query = Nslookup(dns_servers=["1.1.1.1"], verbose=False, tcp=False)
                ips_record = dns_query.dns_lookup(domain)
                l=str(ips_record.answer)
                l=l.replace("'","").replace("[", "").replace("]", "").replace(" ", "")
                l=l.split(",")
                for ip in l:
                    valid_dns_ip.append(ip)
list_of_input_domain=[*set(list_of_input_domain)]
valid_dns_ip=[*set(valid_dns_ip)]
valid_dns_ip.remove("")
print(colored("List of Valid IP from NSlookup and DNS lookup : ","blue"))
print(str(valid_dns_ip)+"\n")
print(colored("List of input domain / DNS : ","blue"))
print(str(list_of_input_domain)+"\n")

#######################

list_of_valid_keyword=[]
with open(r'list_of_keyword.txt', 'r',encoding="utf8") as fp:
            p=0
            # read all lines using readline()
            lines = fp.readlines()
            for row in lines:
                row=row.replace("\n", "")
                list_of_valid_keyword.append(row)
print(colored("List of Keywords to search : ","blue"))
print(str(list_of_valid_keyword)+"\n")
print("-------------------------------------------------\n")

#####################################################
x=input_file.readlines()
total_ip=(len(x))
p=0
n=0
####################################################
def shodan_search(ip):
    try:
        f1=open("temp-file1.txt","w",encoding="utf-8")
        info = api.host(str(ip))
        f1.write(str(info))
        with open(r'temp-file1.txt', 'r',encoding="utf8") as fp1:
            # read all lines using readline()
            lines1 = fp1.readlines()
            for row in lines1:
                for word in list_of_valid_keyword:
                    if row.find(word) != -1:
                        #print("["+str(n)+"/"+str(total_ip)+"] : "+str(ip)+colored(" : Valid from Shodan","green"))
                        table1.add_row([colored(str(n)+"/"+str(total_ip),"white"),str(ip),colored("Valid","green"),colored("Shodan","green")])
                        return True
                    else:
                        return False
    except shodan.APIError as error :   
        pass    
    #    print("["+str(n)+"/"+str(total_ip)+"] : "+str(ip)+colored(" : ","yellow")+colored(error,"yellow"))
    #    return False

def censys_search(ip):
    h = CensysHosts()
    f2=open("temp-file2.txt","r",encoding="utf-8")
    #query = h.search(str(line), per_page=5)               #// Remove comment for censys search
    #f2.write(str(query.view_all()))                       #// Remove comment for censys search
    with open(r'temp-file2.txt', 'r',encoding="utf8") as fp2:
        lines2 = fp2.readlines()
        for row in lines2:
            for word in list_of_valid_keyword:
                if row.find(word) != -1:
                    #print("["+str(n)+"/"+str(total_ip)+"] : "+str(ip)+colored(" : Valid from Censys","green"))
                    table1.add_row([colored(str(n)+"/"+str(total_ip),"white"),str(ip),colored("Valid","green"),colored("Censys","green")])
                    return True
                else:
                    return False
                
def DNS_Recon(ip):
    if ip in valid_dns_ip:
        #print("["+str(n)+"/"+str(total_ip)+"] : "+str(ip)+colored(" : Valid from DNS Lookup","green"))
        table1.add_row([colored(str(n)+"/"+str(total_ip),"white"),str(ip),colored("Valid","green"),colored("DNS+NS lookup","green")])
        return True
    else:
        #print("["+str(n)+"/"+str(total_ip)+"] : "+str(ip)+colored(" : Invalid from ","red")+colored("Shodan, Censys & DNS / NSlookup","yellow"))
        table1.add_row([colored(str(n)+"/"+str(total_ip),"white"),str(ip),colored("Invalid","red"),colored("Shodan, Censys & DNS / NSlookup","red")])
        return False

###################################
input_file=open("ips.txt","r")
x=input_file.readlines()
total_ip=(len(x))   
with Bar('Loading', fill='#', max=total_ip,suffix='%(percent).1f%% - %(eta)ds remaining') as bar:  
    for ip in x:
        n=n+1
        ip=ip.replace("\n", "")
        if shodan_search(ip):
            pass
        elif censys_search(ip):
            pass
        elif DNS_Recon(ip):
            pass
        else:
            pass
        bar.next()
print(table1)