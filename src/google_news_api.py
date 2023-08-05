import requests
from bs4 import BeautifulSoup
import os

class GoogleNewsAPI:
    def __init__(self, api_key, custom_search_engine_id):
        self.api_key = api_key
        self.custom_search_engine_id = custom_search_engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.num_results = 10

    def get_article_text(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract the text content from the article page
            article_text = ' '.join([p.get_text() for p in soup.find_all('p')])
            return article_text.strip()
        except requests.exceptions.RequestException as e:
            print("Error fetching article:", e)
            return ""

    def get_news(self, query):
        params = {
            "key": self.api_key,
            "cx": self.custom_search_engine_id,
            "q": query,
            "num": self.num_results,
            "safe": "active",
            "siteSearch": "https://news.google.com",  # Restrict results to news.google.com domain
            "fields": "items(title,link,pagemap(cse_thumbnail))"
        }

        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            articles = data.get("items", [])
            news_articles=[]
            for article in articles:
                title = article.get("title", "")
                link = article.get("link", "")
                thumbnail = article.get("pagemap", {}).get("cse_thumbnail", [{}])[0].get("src", "")
                article_text = self.get_article_text(link)  # Fetch article content
                news_articles.append({
                    "title":title,
                    "thumbnail":thumbnail,
                    "link":link,
                    "content":article_text
                })

            return news_articles
        except requests.exceptions.RequestException as e:
            print("Error making API request:", e)
            return []

# Replace YOUR_API_KEY with your actual API key

if __name__ == "__main__":
    api_key = os.environ["GOOGLE_SEARCH_API_KEY"]
    search_engine_id = os.environ["GOOGLE_SEARCH_ENGINE_ID"]
    query = "apple"
    google_news_api = GoogleNewsAPI(api_key, search_engine_id)
    news_articles = google_news_api.get_news(query)
    print(news_articles)