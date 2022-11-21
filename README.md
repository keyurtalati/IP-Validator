# IP-Validator
Bulk IP to organization details.

![2022-11-21 10_28_07-image](https://user-images.githubusercontent.com/54932885/202968989-ab08d077-319b-4a21-ad37-079d387ad7d4.png)


# Installation
  1) pip install -r Requirenment.txt
  2) Add your SHODANKEY in the main code ( Line no - 8 )
  3) Configure Censys API & Secret key in your machine (https://github.com/censys/censys-python)
  4) Add IPs in ip.txt file
  5) Add list of domain that are related to target in domain_for_dns.txt
  6) Add list of keyword that are related to target in list_of_keywords.txt
  7) Run the IP-validator.py.
 
# Note
For Censys you will required paid API key, so you can update the code to run shodan code only if you don't have API key for censys.
