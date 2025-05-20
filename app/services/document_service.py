from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader,
    TextLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import os

class DocumentService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def process_file(self, file):
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)
        
        try:
            loader = self._get_loader(temp_path, file.filename)
            if not loader:
                return None
                
            documents = loader.load()
            texts = self.text_splitter.split_documents(documents)
            return texts
            
        finally:
            # Bersihkan file temporary
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
    
    def _get_loader(self, file_path, filename):
        if filename.endswith('.pdf'):
            return PyPDFLoader(file_path)
        elif filename.endswith('.docx'):
            return Docx2txtLoader(file_path)
        elif filename.endswith('.pptx'):
            return UnstructuredPowerPointLoader(file_path)
        elif filename.endswith('.txt'):
            return TextLoader(file_path)
        return None