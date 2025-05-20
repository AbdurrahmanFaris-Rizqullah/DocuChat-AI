from app import create_app
from app.config import OPENAI_API_KEY
import os

def validate_environment():
    """Validasi environment yang diperlukan"""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY tidak ditemukan. "
            "Pastikan Anda telah mengatur variabel lingkungan OPENAI_API_KEY"
        )

def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    try:
        # Validasi environment
        validate_environment()
        
        # Buat aplikasi Flask
        app = create_app()
        
        # Konfigurasi server
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
        
        # Jalankan server
        print(f"Server berjalan di http://{host}:{port}")
        app.run(
            host=host,
            port=port,
            debug=debug
        )
        
    except Exception as e:
        print(f"Error saat menjalankan server: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
