from flask import Blueprint, request, jsonify
from app.services import DocumentService, VectorStoreService, ChatService
from app.config import EMBED_MODE  # Tambahkan import ini
# import os

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
        raw_text = ""
        
        for file in files:
            texts = document_service.process_file(file)
            if texts:
                # Simpan raw text untuk mode tanpa embedding
                raw_text += "\n\n".join([doc.page_content for doc in texts])
                # Simpan texts untuk mode dengan embedding
                all_texts.extend(texts)
        
        if not all_texts:
            return jsonify({
                'error': 'Tidak ada teks yang bisa diekstrak dari file'
            }), 400
            
        # Gunakan EMBED_MODE dari environment
        if EMBED_MODE.lower() == 'true':
            # Mode dengan embedding
            print("Menggunakan mode embedding sesuai konfigurasi")
            vector_store_service.create_vector_store(all_texts)
            print("Berhasil membuat vector store dari dokumen")
            retriever = vector_store_service.get_retriever()
            chain = chat_service.create_chain(retriever) if retriever else None
            response = chat_service.get_response(chain, question)
        else:
            # Mode tanpa embedding (direct text)
            print("Menggunakan mode direct text sesuai konfigurasi")
            prompt = f"Berdasarkan konten berikut:\n\n{raw_text}\n\nJawab pertanyaan ini:\n{question}"
            messages = [{"role": "user", "content": prompt}]
            response = chat_service.llm.invoke(messages).content
    else:
        # Tidak ada file, langsung tanya ke LLM
        chain = None
        response = chat_service.get_response(chain, question)
    
    return jsonify({
        'answer': response
    })