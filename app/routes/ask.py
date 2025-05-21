from flask import Blueprint, request, jsonify
from app.services import DocumentService, VectorStoreService, ChatService

ask_bp = Blueprint('ask', __name__)

# Inisialisasi services
document_service = DocumentService()
vector_store_service = VectorStoreService()
chat_service = ChatService()

@ask_bp.route('/api/ask', methods=['POST'])
def process_and_ask():
    # Cek apakah ada file yang diupload
    has_files = 'files' in request.files
    
    # Cek pertanyaan dari form-data atau json
    question = None
    if request.is_json:
        data = request.get_json()
        question = data.get('question')
    else:
        question = request.form.get('question')
    
    # Jika tidak ada pertanyaan
    if not question:
        return jsonify({
            'error': 'Mohon berikan pertanyaan yang ingin dijawab'
        }), 400
    
    # Proses file jika ada
    if has_files:
        files = request.files.getlist('files')
        all_texts = []
        
        for file in files:
            texts = document_service.process_file(file)
            if texts:
                all_texts.extend(texts)
        
        if all_texts:
            vector_store_service.create_vector_store(all_texts)
            print("Berhasil membuat vector store dari dokumen")
    
    # Proses pertanyaan
    # Jika ada vector store, gunakan untuk konteks
    # Jika tidak ada, gunakan chat biasa
    retriever = vector_store_service.get_retriever()
    if retriever:
        chain = chat_service.create_chain(retriever)
    else:
        chain = None
    
    response = chat_service.get_response(chain, question)
    
    return jsonify({
        'answer': response
    })