import json
from elasticsearch import Elasticsearch,helpers
from dotenv import load_dotenv
import os

class ElasticsearchWrapper:
    def __init__(self):
        load_dotenv()
        # self.es_credentials = {
        #     "url": os.getenv("ELASTIC_URL",None),
        #     "username": os.getenv("ELASTIC_USERNAME",None),
        #     "password": os.getenv("ELASTIC_PASSWORD",None)
        # }
        # print(self.es_credentials)
        # self.client = Elasticsearch(
        #     self.es_credentials["url"],
        #     basic_auth=(self.es_credentials["username"], self.es_credentials["password"]),
        #     verify_certs=False,
        #     request_timeout=3600
        # )
        self.client = Elasticsearch(
            "https://b0f8598dcc5145728dd8e5615508cb6f.us-west1.gcp.cloud.es.io:443",
            api_key="****************************************"
        )

    def create_index(self, index_name, index_body):
        if self.client.indices.exists(index=index_name):
            self.client.indices.delete(index=index_name)
        self.client.indices.create(index=index_name, body=index_body)

    def add_document(self, index_name, doc):
        self.client.index(index=index_name, body=doc)
    
    def ingest_bulk(self,index,documents):
        index_documents = [{"_index":index, "_source":source} for source in documents]
        helpers.bulk(self.client,index_documents)

    def text_to_chunks(self,texts: str,
                    fix_prefix:str = "",
                    chunk_length: int = 256,
                    chunk_overlap: int = 0) -> list:
        """
        Splits the text into equally distributed chunks with 50% overlap.
        Args:
            texts (str): Text to be converted into chunks.
            chunk_length (int): Maximum number of words in each chunk.
            chunk_overlap (int): Number of words to overlap between chunks.
        """
        words = texts.split(' ')
        n = len(words)
        chunks = []
        i = 0
        while i < n:  # Corrected the length check
            chunk = words[i: min(i + chunk_length, n)]
            i = i + chunk_length - chunk_overlap
            #print(len(chunk))
            chunk = ' '.join(chunk).strip()
            chunks.append(fix_prefix + chunk)
        return chunks

    def load_and_index_documents(self, index_name, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            documents = []
            for item in data:
                full_text =  item['main_content']  # Full article content
                chunks = self.text_to_chunks(texts=full_text,fix_prefix="",chunk_length=256,chunk_overlap=0)
                for i, chunk in enumerate(chunks):
                    doc = {
                        "text": str(item.get('article_metadata', {})) + chunk,
                        "chunk_number": i + 1,
                        "url": item.get('url', 'N/A'),  # Safely get URL or default if not present
                        "article_metadata": item.get('article_metadata', {}),  # Safely get metadata or default if not present
                        "main_content": full_text
                    }
                    self.add_document(index_name=index_name,doc=doc)
                    documents.append(doc)
            self.ingest_bulk(index=index_name,documents=documents)

if __name__ == "__main__":
    es_wrapper = ElasticsearchWrapper()
    es_wrapper.create_index("knowledge_base_src", {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "chunk_number": {"type": "integer"},
                "url": {"type": "text"},  
                "article_metadata": {"type": "text"},  
                "main_content": {"type": "text"}  
            }
        }
    })
    es_wrapper.load_and_index_documents("knowledge_base_src", "./knowledge_base_docs.json")    
