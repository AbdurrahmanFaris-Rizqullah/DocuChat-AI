# GPT Document Chat API

API ini memungkinkan pengguna untuk melakukan chat dengan dokumen menggunakan teknologi GPT. Sistem ini mendukung berbagai format dokumen dan dapat memberikan respons berdasarkan konten dokumen.

## Persyaratan Sistem

- Python 3.x
- OpenAI API Key

## Instalasi

1. Clone repositori ini
2. Buat file `.env` di root direktori dan tambahkan OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```
3. bikin venv terlebih dahulu
```bash
python -m venv venv
```
4. Aktifkan venv:
```bash
source venv/bin/activat
```

5. Install dependensi:
```bash
pip install -r requirements.txt
```

## Format Dokumen yang Didukung
Api ini mendukung berbagai format dokumen, termasuk:
- PDF
- DOCX
- TXT
- PPTX

## Menjalankan API
Untuk menjalankan API, jalankan perintah berikut:
```bash
python server.py
```
Server akan berjalan di ```localhost:5000.```

## Endpoint API
Endpoint ini digunakan untuk melakukan chat, serta menganalis isi dokumen. Bisa menggunakan raw ataupun body form di postman.
```Post
localhost:5000/api/ask
```
## Contoh Request 
1. Bila ingin melakukan Chat, gunakan endpoint berikut:
```json
{
    "question": "Bagaimana cara menggunakan API ini?",
}
```

2. Bila ingin menganalisis isi dokumen, gunakan endpoint berikut:
```json
{
    "question": "Apa isi dokumen ini?",
    "files": "path/to/your/document.pdf"
}
```

## Eksekusi mas dicky / mas rafi xixiixixix