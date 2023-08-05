from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

class Embeddings:
    def __init__(self):
        self.OPENAI_API_KEY=os.environ["OPENAI_API_KEY"]
        self.embedding = OpenAIEmbeddings(openai_api_key=self.OPENAI_API_KEY)

    def create_article_index(self, articles, domain):
        rec_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, 
                                              chunk_overlap=150)
        web_docs, meta = [], []
        for article in tqdm(articles, desc="Splitting articles into chunks"):
            splits = rec_splitter.split_text(article["content"])
            web_docs.extend(splits)
            meta.extend([{
                    "title":article['title'],
                    "thumbnail":article['thumbnail'],
                    "source":article['link']
                }] * len(splits))
        article_store = FAISS.from_texts(
            texts=web_docs, embedding = self.embedding, metadatas=meta
        )
        article_store.save_local("indices/INDEX-"+domain)
        return article_store
    
    def load_article_index(self, article_index):
        return FAISS.load_local(article_index, self.embedding)
