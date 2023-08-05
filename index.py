# Import required modules
from src.domain import Domain
from src.google_news_api import GoogleNewsAPI
from src.embeddings import Embeddings
from src.prompts import Prompts
import os
import json

# Main class 'Index' which carries out the entire logic
class Index:
    def __init__(self):
        # Initialize API key and search engine ID from environment variables
        self.api_key = os.environ["GOOGLE_SEARCH_API_KEY"]
        self.search_engine_id = os.environ["GOOGLE_SEARCH_ENGINE_ID"]
        # Define a list of event types for structured information extraction
        self.EVENT_TYPES = ['product_launch', 'partnership', 'investment_received', 'investment_made', 'new_hire', 'issues', 'competitor_found']

# The following code executes only if this script is run as the main module
if __name__ == "__main__":
    # Create a string of dashes to be used for visual separation
    dashes = "-" * 30

    # Create instances of required classes
    domain = Domain()
    index = Index()
    embed = Embeddings()

    # Get the domain name from the user
    domain_name = input("Enter the domain name of the company: ")

    # Check if the domain is registered or not
    is_registered = domain.is_registered(domain_name)

    if is_registered:
        # Get domain information for the entered domain name
        domain_info = domain.get_domain_info(domain_name)

        if domain_info:
            # Print domain information
            print(f'{dashes} domain info {dashes}')
            for key, value in domain_info.items():
                print(f"{key}: {value}")

        # Extract the company name from the domain information
        company_name = domain_info['org']

        # Fetch news articles related to the domain and company
        print(f'{dashes} crawling news articles from google {dashes}')
        google_news_api = GoogleNewsAPI(index.api_key, index.search_engine_id)
        articles=[]
        for start in range(1,2):
            if company_name != None:
                articles.extend(google_news_api.get_news(company_name, (10*start)+1 ))
            articles.extend(google_news_api.get_news(domain_name, (10*start)+1 ))
        
        print(f'crawling news articles [DONE]')

        # Create article embeddings and index using FAISS
        print(f'{dashes} creating article index {dashes}')
        article_index = embed.create_article_index(articles, domain_name)
        print(f'article index [CREATED] and stored in the folder named indices.')

        # Extract structured information using LLM prompt engineering
        if os.path.exists("indices/INDEX-" + domain_name):
            embed = Embeddings()
            p = Prompts()
            print(f'{dashes} loading embeddings {dashes}')
            article_index = embed.load_article_index("indices/INDEX-" + domain_name)
            print(f'embeddings loaded')

            # Dictionary to store structured information for each event type
            events = {}

            # Loop through each event type and answer questions using prompt engineering
            for event_type in p.EVENT_TYPES:
                print(f'{dashes} answering questions for the event type {event_type} {dashes}')
                output = p.question_answering(event_type, article_index)
                events[event_type] = output
                print(f'questions for {event_type} answered [SUCCESSFULLY]')

            # Save the structured information to a JSON file
            with open("output.json", "w") as outfile:
                json.dump(events, outfile)
        else:
            print("index not available. Please create one.")

    else:
        print(f'{domain_name} is not registered.')