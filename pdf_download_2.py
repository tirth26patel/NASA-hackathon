import os
import time
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Path to your CSV
csv_path = "SB_publication_PMC.csv"
df = pd.read_csv(csv_path)

link_column = "Link"

# Setup Chrome
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

output_folder = "datasets"
os.makedirs(output_folder, exist_ok=True)

for idx, url in enumerate(df[link_column].dropna(), start=1):
    try:
        print(f"[{idx}] Visiting: {url}")
        driver.get(url)

        # Wait for POW challenge to finish
        time.sleep(8)

        # Find PDF link
        pdf_link = None
        links = driver.find_elements(By.TAG_NAME, "a")
        for a in links:
            href = a.get_attribute("href")
            if href and "pdf" in href.lower():
                pdf_link = href
                break

        if not pdf_link:
            print("❌ PDF link not found.")
            continue

        # Fix malformed URLs
        pdf_link = pdf_link.replace("pmc.ncbi.nlm.nih.govv", "pmc.ncbi.nlm.nih.gov")
        pdf_link = pdf_link.replace("//articles", "/articles")

        print(f"📥 Opening PDF page: {pdf_link}")
        driver.get(pdf_link)

        # Wait for POW cookie to appear
        time.sleep(6)

        # Grab cookies from Selenium
        cookies = {c['name']: c['value'] for c in driver.get_cookies()}

        # Build headers
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": url,
        }

        # Download actual PDF with requests
        resp = requests.get(pdf_link, headers=headers, cookies=cookies, timeout=30)
        resp.raise_for_status()

        # Save file
        pdf_path = os.path.join(output_folder, f"NASA_paper_{idx}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(resp.content)

        print(f"✅ Saved real PDF: {pdf_path}")
        time.sleep(2)

    except Exception as e:
        print(f"⚠️ Failed to download {url}: {e}")

driver.quit()
print("\n🎉 Finished downloading all available PDFs.")
