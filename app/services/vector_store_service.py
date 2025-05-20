from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.config import OPENAI_API_KEY

class VectorStoreService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.vector_store = None
    
    def create_vector_store(self, documents):
        if not documents:
            return None
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        return self.vector_store
    
    def get_retriever(self):
        if not self.vector_store:
            return None
        return self.vector_store.as_retriever()