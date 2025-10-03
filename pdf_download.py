import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin

# Path to your CSV
csv_path = "SB_publication_PMC.csv"

# Folder to save PDFs
output_folder = "datasets"
os.makedirs(output_folder, exist_ok=True)

# Load CSV
df = pd.read_csv(csv_path)

# Inspect columns first
print("Columns:", df.columns)

# Replace with the column that contains the webpage URLs
link_column = "Link"   # <-- Change this after checking the print output

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

for idx, page_url in enumerate(df[link_column].dropna(), start=1):
    try:
        print(f"\n[{idx}] Visiting: {page_url}")
        page = requests.get(page_url, headers=headers, timeout=20)
        page.raise_for_status()

        soup = BeautifulSoup(page.text, "html.parser")

        # Common patterns for PMC / journal pages
        pdf_link = None
        for a in soup.find_all("a", href=True):
            if "pdf" in a.get("href").lower():
                pdf_link = urljoin(page_url, a.get("href"))
                break
        
        if not pdf_link:
            print("❌ No PDF link found on this page.")
            continue

        print(f"📥 Downloading PDF from: {pdf_link}")
        pdf_response = requests.get(pdf_link, headers=headers, timeout=30)
        pdf_response.raise_for_status()

        # Save PDF
        pdf_filename = f"NASA_paper_{idx}.pdf"
        pdf_path = os.path.join(output_folder, pdf_filename)

        with open(pdf_path, "wb") as f:
            f.write(pdf_response.content)

        print(f"✅ Saved: {pdf_filename}")

        time.sleep(1)  # be polite to servers

    except Exception as e:
        print(f"⚠️ Failed at {page_url}: {e}")

print(f"\n🎉 All PDFs downloaded to: {output_folder}")
