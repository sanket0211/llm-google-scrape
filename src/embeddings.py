# Import necessary modules
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Define a class named 'Embeddings'
class Embeddings:
    def __init__(self):
        # Initialize the OpenAI API key from the environment variable
        self.OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
        # Create an instance of the OpenAIEmbeddings class with the API key
        self.embedding = OpenAIEmbeddings(openai_api_key=self.OPENAI_API_KEY)

    def create_article_index(self, articles, domain):
        # Create a RecursiveCharacterTextSplitter instance with specified chunk size and overlap
        rec_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
        # Lists to store split text chunks and their corresponding metadata
        web_docs, meta = [], []
        # Iterate through each article and split its content into chunks
        for article in tqdm(articles, desc="Splitting articles into chunks"):
            splits = rec_splitter.split_text(article["content"])
            # Extend the lists with the split chunks and their metadata
            web_docs.extend(splits)
            meta.extend([{
                    "title": article['title'],
                    "thumbnail": article['thumbnail'],
                    "source": article['link'] + '|' + article['local_path'],
                    "local_path": article['local_path']
                }] * len(splits))
        # Create an FAISS vector store from the split text chunks and their metadata
        article_store = FAISS.from_texts(
            texts=web_docs, embedding=self.embedding, metadatas=meta
        )
        # Save the article store locally with a filename based on the domain
        article_store.save_local("indices/INDEX-"+domain)
        # Return the article store
        return article_store
    
    def load_article_index(self, article_index):
        # Load an FAISS vector store from a local file based on the given article_index and embedding
        return FAISS.load_local(article_index, self.embedding)