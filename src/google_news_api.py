# Import necessary modules
import requests
from bs4 import BeautifulSoup
import os
import string
import random

# Define a class named 'GoogleNewsAPI'
class GoogleNewsAPI:
    def __init__(self, api_key, custom_search_engine_id):
        # Initialize the API key and custom search engine ID
        self.api_key = api_key
        self.custom_search_engine_id = custom_search_engine_id
        # Set the base URL for making requests to the Google Custom Search API
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        # Set the number of results to retrieve (default is 10)
        self.num_results = 10

    def random_alphanumeric_string(self, length):
        return ''.join(
            random.choice(string.ascii_lowercase + string.digits)
            for _ in range(length)
    )

    def get_article_text(self, url):
        try:
            # Send a GET request to fetch the article page
            response = requests.get(url)
            # Parse the HTML content of the article page using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract the text content from the article page (joining all <p> tags)
            article_text = ' '.join([p.get_text() for p in soup.find_all('p')])
            return article_text.strip()  # Return the article text after stripping leading/trailing spaces
        except requests.exceptions.RequestException as e:
            # If there is an error fetching the article, print the error and return an empty string
            print("Error fetching article:", e)
            return ""

    def get_news(self, query, start):
        # Define parameters for the Google Custom Search API request
        params = {
            "key": self.api_key,
            "cx": self.custom_search_engine_id,
            "q": query,  # The search query
            "num": self.num_results,  # The number of results to retrieve
            "safe": "active",  # SafeSearch setting: 'active' filters explicit content
            "siteSearch": "https://news.google.com",  # Restrict results to news.google.com domain
            "fields": "items(title,link,pagemap(cse_thumbnail))",  # Only retrieve specific fields for each item
            "start": start
        }
        isExist = os.path.exists("dump")
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs("dump")
            print("The new dump directory is created!")
        data_dump_path = "dump/"+ self.random_alphanumeric_string(10)
        isExist = os.path.exists(data_dump_path)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(data_dump_path)
            print("The query dump directory is created!")

        try:
            # Send a GET request to the Google Custom Search API with the defined parameters
            response = requests.get(self.base_url, params=params)
            # Parse the response data as JSON
            data = response.json()
            # Get the list of articles from the response (if available, otherwise an empty list)
            articles = data.get("items", [])
            # Initialize an empty list to store news articles and their content
            news_articles = []
            # Loop through each article in the response and extract relevant information
            for article in articles:
                title = article.get("title", "")
                link = article.get("link", "")
                thumbnail = article.get("pagemap", {}).get("cse_thumbnail", [{}])[0].get("src", "")
                # Fetch the full content of the article using the 'get_article_text' method
                article_text = self.get_article_text(link)
                # Append the article information to the 'news_articles' list
                fname=self.random_alphanumeric_string(10)
                with open (data_dump_path+'/'+fname + '.txt', 'w') as file:  
                    file.write(title + "\n" + link + "\n" + article_text + '\n')  
                news_articles.append({
                    "title": title,
                    "thumbnail": thumbnail,
                    "link": link,
                    "content": article_text, 
                    "local_path": data_dump_path+'/'+fname + '.txt'
                })

            return news_articles  # Return the list of news articles and their content
        except requests.exceptions.RequestException as e:
            # If there is an error making the API request, print the error and return an empty list
            print("Error making API request:", e)
            return []

# The following code executes only if this script is run as the main module
if __name__ == "__main__":
    # Retrieve the API key and custom search engine ID from environment variables
    api_key = os.environ["GOOGLE_SEARCH_API_KEY"]
    search_engine_id = os.environ["GOOGLE_SEARCH_ENGINE_ID"]
    # Set the search query (in this case, "apple")
    query = "apple"
    # Create an instance of the 'GoogleNewsAPI' class with the API key and search engine ID
    google_news_api = GoogleNewsAPI(api_key, search_engine_id)
    # Call the 'get_news' method to retrieve news articles related to the search query
    news_articles = google_news_api.get_news(query)
    # Print the list of news articles and their content
    print(news_articles)