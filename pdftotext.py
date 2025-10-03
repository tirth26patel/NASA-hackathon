import os
from PyPDF2 import PdfReader

PDF_DIR = r"C:\Users\Kavan\OneDrive\Desktop\Hackathon\project\experiments"
OUTPUT_DIR = r"C:\Users\Kavan\OneDrive\Desktop\Hackathon\project\pdf_texts"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

def convert_all_pdfs():
    for filename in os.listdir(PDF_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, filename)
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(OUTPUT_DIR, txt_filename)

            print(f"📄 Processing: {filename}")
            text = extract_text_from_pdf(pdf_path)

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"✅ Saved: {txt_path}")

if __name__ == "__main__":
    convert_all_pdfs()
