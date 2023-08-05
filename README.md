# Domain Information and News Analysis

This project consists of several Python scripts to extract domain information, crawl news articles from Google News API, create article embeddings, and perform structured information extraction using LLM prompt engineering.

## Prerequisites

To run the scripts in this project, you need to have the following:

- Python 3.x
- Required Python packages (can be installed using `pip install -r requirements.txt`)
- Environment variables set for the following:
  - `GOOGLE_SEARCH_API_KEY`: API key for the Google Custom Search API
  - `GOOGLE_SEARCH_ENGINE_ID`: Custom search engine ID for Google News API
  - `OPENAI_API_KEY`: API key for OpenAI

## Setup

1. Clone the repository to your local machine:

```bash
git clone <repository_url>
cd domain-news-analysis
```
2. install the required packages:

```bash
pip install -r requirements.txt
```

3. Set the necessary environment variables with your API keys.

## Usage

# Index.py
The index.py script is the main script that drives the entire process of domain information extraction, news crawling, embeddings creation, and structured information extraction.

```bash 
python index.py
```

The script will prompt you to enter the domain name of a company. It will then check if the domain is registered, and if it is, it will fetch domain information and crawl news articles related to the domain and the company name (if available). The crawled articles will be used to create embeddings and then indexed using FAISS.

# Domain.py
The domain.py script contains the Domain class, which provides functionality to check if a domain is registered and fetch domain information.

# GoogleNewsAPI.py
The google_news_api.py script contains the GoogleNewsAPI class, which interacts with the Google News API to fetch news articles related to a given query.

# Embeddings.py
The embeddings.py script contains the Embeddings class, which handles OpenAI embeddings and creates an article index using FAISS.

# Prompts.py
The prompts.py script contains the Prompts class, which performs structured information extraction using LLM prompt engineering.

# Output

The output of the script will be structured information for different event types saved in a JSON file named output.json. The output will be stored in the following format:

```bash
{
  "event_type_1": {
    "question_1": "answer_1",
    "question_2": "answer_2",
    ...
  },
  "event_type_2": {
    "question_1": "answer_1",
    "question_2": "answer_2",
    ...
  },
  ...
}
```
## License

This project is licensed under the MIT License.








