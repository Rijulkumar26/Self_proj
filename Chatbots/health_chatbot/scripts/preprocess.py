import os
import json
import fitz  # PyMuPDF
import re
from tqdm import tqdm

RAW_DIR = "data/raw/uhc_policies"
OUTPUT_FILE = "data/processed/chunks.json"

os.makedirs("data/processed", exist_ok=True)


# ----------- TEXT EXTRACTION ----------- #
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


# ----------- CLEANING ----------- #
def clean_text(text):
    text = re.sub(r"\n+", "\n", text)  # remove extra newlines
    text = re.sub(r"\s+", " ", text)   # normalize spaces
    return text.strip()


# ----------- SECTION SPLITTING ----------- #
SECTION_PATTERNS = [
    "Coverage Rationale",
    "Coverage Criteria",
    "Definitions",
    "Applicable Codes",
    "Limitations",
    "Policy",
    "Indications",
    "Documentation Requirements",
    "References"
]


def split_into_sections(text):
    sections = []

    # Create regex pattern
    pattern = "|".join([f"({sec})" for sec in SECTION_PATTERNS])

    matches = list(re.finditer(pattern, text, re.IGNORECASE))

    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        section_title = matches[i].group().strip()
        section_text = text[start:end].strip()

        sections.append({
            "section": section_title,
            "content": section_text
        })

    # fallback if no sections found
    if not sections:
        sections.append({
            "section": "Full Document",
            "content": text
        })

    return sections


# ----------- MAIN PIPELINE ----------- #
def process_pdfs():
    all_data = []

    pdf_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".pdf")]

    for pdf_file in tqdm(pdf_files):
        pdf_path = os.path.join(RAW_DIR, pdf_file)

        try:
            raw_text = extract_text_from_pdf(pdf_path)
            cleaned_text = clean_text(raw_text)
            sections = split_into_sections(cleaned_text)

            for sec in sections:
                all_data.append({
                    "policy_name": pdf_file.replace(".pdf", ""),
                    "section": sec["section"],
                    "content": sec["content"],
                    "source_file": pdf_file
                })

        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")

    # Save output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)

    print(f"Saved processed data to {OUTPUT_FILE}")


if __name__ == "__main__":
    process_pdfs()