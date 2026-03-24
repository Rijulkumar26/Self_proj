import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

BASE_URL = "https://www.uhcprovider.com"
PAGE_URL = "https://www.uhcprovider.com/en/policies-protocols/commercial-policies/commercial-medical-drug-policies.html"

SAVE_DIR = "data/raw/uhc_policies"
os.makedirs(SAVE_DIR, exist_ok=True)


def get_policy_links():
    response = requests.get(PAGE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []

    h5_tags = soup.find_all("h5", class_="list-title")

    for tag in h5_tags:
        a_tag = tag.find("a")
        if a_tag and "href" in a_tag.attrs:
            pdf_url = urljoin(BASE_URL, a_tag["href"])
            title = a_tag.text.strip()

            links.append({
                "title": title,
                "url": pdf_url
            })

    return links


def download_pdfs(links):
    for link in tqdm(links):
        title = link["title"].replace("/", "-")
        file_name = f"{title}.pdf"
        file_path = os.path.join(SAVE_DIR, file_name)

        try:
            pdf_response = requests.get(link["url"])

            with open(file_path, "wb") as f:
                f.write(pdf_response.content)

        except Exception as e:
            print(f"Failed: {title} -> {e}")


if __name__ == "__main__":
    print("Fetching policy links...")
    links = get_policy_links()
    print(f"Found {len(links)} policies")

    print("Downloading PDFs...")
    download_pdfs(links)

    print("Completed scrapping")