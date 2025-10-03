for idx, row in df.iterrows():
    pmc_url = str(row[pdf_column])
    if not pmc_url.startswith("http"):
        print(f"Skipping row {idx}: invalid URL → {pmc_url}")
        continue

    # Convert article page URL to PDF URL
    if "ncbi.nlm.nih.gov/pmc/articles/" in pmc_url:
        if not pmc_url.endswith("/"):
            pmc_url += "/"
        pdf_url = pmc_url + "pdf"
    else:
        pdf_url = pmc_url   # in case some links are already PDF
    
    # Derive a filename
    parsed = urlparse(pdf_url)
    fname = os.path.basename(parsed.path)
    if fname == "pdf":  # handle PMC pdf endpoint
        fname = f"PMC_{idx}.pdf"

    out_path = os.path.join(output_folder, fname)

    # Download the PDF
    try:
        print(f"Downloading {pdf_url} → {out_path}")
        pdf_resp = requests.get(pdf_url, timeout=30)
        pdf_resp.raise_for_status()
        with open(out_path, "wb") as f:
            f.write(pdf_resp.content)
        print("✅ Success")
    except Exception as e:
        print(f"❌ Failed for {pdf_url}: {e}")
