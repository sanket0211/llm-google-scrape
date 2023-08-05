from src.domain import Domain
from src.google_news_api import GoogleNewsAPI
from src.embeddings import Embeddings
from src.prompts import Prompts
import os
import json

class Index:
    def __init__(self):
        self.api_key = os.environ["GOOGLE_SEARCH_API_KEY"]
        self.search_engine_id = os.environ["GOOGLE_SEARCH_ENGINE_ID"]
        self.EVENT_TYPES = ['product_launch', 'partnership', 'investment_received', 'investment_made', 'new_hire', 'issues', 'competitor_found']

if __name__ == "__main__":
    dashes = "-"*30
    domain = Domain()
    index = Index()
    embed = Embeddings()
    domain_name = input("Enter the domain name of the company: ")
    is_registered = domain.is_registered(domain_name)
    if is_registered:
        domain_info = domain.get_domain_info(domain_name)
        
        if domain_info:
            print(f'{dashes} domain info {dashes}')
            for key, value in domain_info.items():
                print(f"{key}: {value}")
        company_name = domain_info['org']
        print(f'{dashes} crawling news articles from google {dashes}')
        google_news_api = GoogleNewsAPI(index.api_key, index.search_engine_id)
        articles = google_news_api.get_news(domain_name)
        if company_name != None:
            articles.extend(google_news_api.get_news(company_name))
        print(f'crawling news articles [DONE]')
        print(f'{dashes} creating article index {dashes}')
        article_index = embed.create_article_index(articles, domain_name)
        
        print(f'article index [CREATED] and stored in the folder named indices.')

        if os.path.exists("indices/INDEX-" +domain_name ):
            embed = Embeddings()
            p = Prompts()
            print(f'{dashes} loading embeddings {dashes}')
            article_index = embed.load_article_index("indices/INDEX-" +domain_name)
            print(f'embeddings loaded')
            events = {}
            for event_type in p.EVENT_TYPES:
                print(f'{dashes} answering questions for the event type {event_type} {dashes}')
                output = p.question_answering(event_type, article_index)
                events[event_type] = output
                print(f'questions for {event_type} answered [SUCCESSFULLY]')
            with open("output.json", "w") as outfile:
                json.dump(events, outfile)
        else:
            print("index not available. Please create one.")

    else:
        print(f'{domain_name} is not registered.')