# 🔍 Fireworks KYC Document Extraction PoC

This project is a working end-to-end PoC that demonstrates how Fireworks AI can be used to extract identity information from real-world documents like passports and driver’s licenses. The goal is to support **KYC workflows** by automating text extraction and transforming it into clean, structured data — without templates or traditional OCR pipelines.

The solution uses a two-step LLM pipeline:

1. **Vision-Language model (OCR)** → Extract text from the uploaded image using OCR  
2. **Text model (Parsing)** → Convert the extracted text into structured JSON format

---

## 🚀 Features

- 📄 Extract text from identity documents using Fireworks Vision models  
- 🤖 Convert OCR text to structured JSON identity fields  
- 🗂 Supports multiple document types (Passports & Driver Licenses)  
- 🔁 Batch processing mode (process all documents automatically)  
- 🖥 Streamlit UI for user-friendly uploads (Optional)
- 💾 Outputs automatically stored in `/outputs/`  

---

## 🧠 Architecture Overview

```plaintext
Document Image
      │
      ▼
Qwen2.5-VL-32B (OCR Model)
      │
      ▼
Extracted Raw Text
      │
      ▼
Llama-3.1-8B-Instruct (Parser Model)
      │
      ▼
Structured JSON Output
      │
      ▼
Saved to /outputs/
```


## ⚙️ Setup

1. Install dependencies:

```sh
pip install -r requirements.txt
```
Create a .env file and add your Fireworks API key:

```env
Copy code
FIREWORKS_API_KEY=your_api_key_here
```

▶️ How to Run It
🚀 Batch Mode (Processes everything in /samples/)
```sh
python src/main.py
Each processed document will create a JSON file inside /outputs/.
```

🖥 Streamlit UI (Interactive Mode)
```sh
Copy code
streamlit run app.py
Then visit:

👉 http://localhost:8501
Upload any supported document and view the structured output instantly.
```

📦 Example Output
```json
Copy code
{
  "full_name": "JOHN DOE",
  "dob": "1996-03-15",
  "expiry_date": "2027-04-14",
  "document_number": "963545637",
  "sex": "M",
  "nationality": "USA",
  "address": null,
  "document_type": "Passport"
}
```
## 💡 Why These Models?
Qwen2.5 Vision Model does well at extracting readable text from documents with varying layouts, fonts, and backgrounds.

Llama-3.1-8B-Instruct is ideal for parsing and formatting text logically into consistent JSON — without unnecessary compute.


## 🔧 Known Gaps
This is a PoC, so a few things are intentionally out of scope:

No automated validation for the pictures

No fraud detection / watermark consistency checks

No cross-document face comparison

No confidence scoring

These would be the next logical steps in a production-ready system.

## 🚀 Future Enhancements
- Face matching between multiple documents	
- Identity verification confidence
- Document format validation rules	
- Reduce false positives
- Confidence scoring per field	
- Useful for risk scoring
- Storage and audit logging	