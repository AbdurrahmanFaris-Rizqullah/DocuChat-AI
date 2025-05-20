from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
from app.config import OPENAI_API_KEY

class ChatService:
    def __init__(self):
        self.chat_history = []
        self.llm = ChatOpenAI(
            temperature=0,
            openai_api_key=OPENAI_API_KEY
        )
    
    def create_chain(self, retriever):
        if not retriever:
            return None
            
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            return_source_documents=True,
            get_chat_history=lambda h: h
        )
    
    def get_response(self, chain, question):
        if not chain:
            return "Mohon upload file terlebih dahulu."
        
        # Konfigurasi untuk menyimpan riwayat chat    
        config = RunnableConfig(
            configurable={
                "chat_history": self.chat_history
            }
        )
        
        # Jalankan chain dengan konfigurasi
        response = chain.invoke(
            {"question": question},
            config=config
        )
        
        # Simpan pesan ke riwayat
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=response['answer']))
        
        return response['answer']