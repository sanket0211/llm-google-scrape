import requests
import whois

class Domain:
    def __init__(self):
        self.base_url = 'https://api.whois-v0.com'
        self.endpoint = '/whois'

    def is_registered(self, domain_name):
        """
        A function that returns a boolean indicating 
        whether a `domain_name` is registered
        """
        try:
            w = whois.whois(domain_name)
        except Exception as e:
            return False
        else:
            return bool(w.domain_name)


    def get_domain_info(self, domain_name):
        try:
            w = whois.whois(domain_name)
        except Exception as e:
            return False
        else:
            return w

if __name__ == "__main__":
    domain = Domain()
    domain_name = input("Enter the domain name of the company: ")
    is_registered = domain.is_registered(domain_name)
    if is_registered:
        domain_info = domain.get_domain_info(domain_name)

        if domain_info:
            print("Company Information:")
            for key, value in domain_info.items():
                print(f"{key}: {value}")
    else:
        print(f'{domain_name} is not registered.')