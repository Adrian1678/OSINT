import socket
import whois
import dns.resolver
import argparse
parse=argparse.ArgumentParser(description="OSINT")
parse.add_argument("-d","--domain")
parse.add_argument("-s","--subdomain")
parse.add_argument("-o","--output")

args=parse.parse_args()

target=args.domain
subdomain_file=args.subdomain
output=args.output
#function that gets the ip address of a domain
def get_ip(domain):
    ip= socket.gethostbyname(domain)
    pr=(f"{domain}'s IP address is: {ip}")
    print(pr)
    if output:
        with open(output, "a") as o:
            o.write(pr + "\n")
    return ip

#pulling whois domains information
def get_whois(domain):
    data=whois.whois(domain)
    #fixing the date format
    created=data.creation_date
    expires=data.expiration_date
    if isinstance(created, list):
        created=created[0]
        if isinstance(expires, list):
            expires= expires[0]
            #setting up the print and variables so i can paste it on a file
    pr_one=(f"[+] Registrar:      {data.registrar}")
    print(pr_one)
    pr_two=(f"[+] Created:        {created.strftime('%Y-%m-%d')}")
    print(pr_two)
    pr_three=(f"[+] Expires:        {expires.strftime('%Y-%m-%d')}")
    print(pr_three)
    pr_four=(f"[+] Nameservers:    {data.name_servers}")
    print(pr_four)
    pr_five=("------------------------------------------------")
    print(pr_five)
    #pasting everything into the file
    if output:
        with open(output, "a")as o:
            o.write(pr_one + "\n")
            o.write(pr_two + "\n")
            o.write(pr_three + "\n")
            o.write(pr_four + "\n")
            o.write(pr_five + "\n")
    return data


#function to pull up DNS information
def get_dns(domain):
    for record_type in ["A", "MX", "NS", "TXT"]:
        try:
            answers= dns.resolver.resolve(domain, record_type)
            for record in answers:
                pr_one=(f"[+] {record_type}: {record}")
                print(pr_one)
                if output:
                    with open(output, "a") as o:
                        o.write(pr_one +"\n")
        except:
            pr_two=(f"[+] no {record_type} records found")
            print(pr_two)
            if output:
                with open(output, "a") as o:
                    o.write(pr_two +"\n")
        pr_three=("---------------------------------------")
        print(pr_three)
        # pasting everything into the users file if output is True
        if output:
            with open(output, "a") as o:
                
                o.write(pr_three + "\n")
                
    return

#function to test different subdomains
def get_subdomains(domain,subdomain):
    #combining the subdomain and domain to sent to the testlab
    full_domain=f"{subdomain}.{domain}"
    try:
        ip= socket.gethostbyname(full_domain)
        pr_one=(f"[+] Found: {full_domain}--> {ip}")
        if output:
            with open(output, "a") as o:
                o.write(pr_one + "\n")
    except:
        pass


get_ip(target)
get_whois(target)
get_dns(target)


#creating a file to search for subdomains

with open(subdomain_file, "r") as wordlist:
    for subdomain in wordlist:
        #striping the words so there is no space
        subdomain=subdomain.strip("\n")
        get_subdomains(target,subdomain)

