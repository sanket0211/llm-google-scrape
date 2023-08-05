# Import the 'whois' module which is used to query domain registration information
import whois

# Define a class named 'Domain'
class Domain:
    def __init__(self):
        # Initialize the base URL and endpoint for the WHOIS API
        self.base_url = 'https://api.whois-v0.com'
        self.endpoint = '/whois'

    def is_registered(self, domain_name):
        """
        A function that returns a boolean indicating
        whether a `domain_name` is registered

        :param domain_name: The name of the domain to check for registration
        :return: True if the domain is registered, False otherwise
        """
        try:
            # Use the 'whois' module to get WHOIS information for the domain
            w = whois.whois(domain_name)
        except Exception as e:
            # If an exception occurs (e.g., domain not found), return False
            return False
        else:
            # If WHOIS information is successfully retrieved, check if 'domain_name' is present in the response
            return bool(w.domain_name)

    def get_domain_info(self, domain_name):
        """
        A function that returns WHOIS information for a given `domain_name`

        :param domain_name: The name of the domain to fetch WHOIS information for
        :return: WHOIS information as a dictionary or False if an error occurs
        """
        try:
            # Use the 'whois' module to get WHOIS information for the domain
            w = whois.whois(domain_name)
        except Exception as e:
            # If an exception occurs (e.g., domain not found), return False
            return False
        else:
            # If WHOIS information is successfully retrieved, return it as a dictionary
            return w

if __name__ == "__main__":
    # Create an instance of the 'Domain' class
    domain = Domain()

    # Get the domain name from the user
    domain_name = input("Enter the domain name of the company: ")

    # Check if the domain is registered
    is_registered = domain.is_registered(domain_name)

    if is_registered:
        # If the domain is registered, get its WHOIS information
        domain_info = domain.get_domain_info(domain_name)

        if domain_info:
            # If WHOIS information is available, print it
            print("Company Information:")
            for key, value in domain_info.items():
                print(f"{key}: {value}")
    else:
        # If the domain is not registered, inform the user
        print(f'{domain_name} is not registered.')