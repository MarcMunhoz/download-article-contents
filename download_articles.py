import requests
from bs4 import BeautifulSoup
import openpyxl
import os
from urllib.parse import urlparse

# Path to the XLSX file
xlsx_path = "path/to/spreadsheet.xlsx"

# Function to download content from a URL
def download_article_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

# Function to extract article content from HTML
def extract_article_content(html):
    soup = BeautifulSoup(html, "html.parser")
    # BeautifulSoup methods to extract the article content
    article_content = soup.find("article").prettify()
    #Structure of the target website
    return article_content

# Main function
def main():
    workbook = openpyxl.load_workbook(xlsx_path)
    sheet = workbook.active
    
    for row in sheet.iter_rows(min_row=2, max_col=1, values_only=True):
        url = row[0]
        html_content = download_article_content(url)
        if html_content:
            article_content = extract_article_content(html_content)
            if article_content:
                # Get the last part of the URL path and use it as the filename
                url_path = urlparse(url).path
                filename = os.path.basename(url_path)
                
                # Remove invalid characters from the filename
                filename = filename.replace('/', '_')
                
                # Save article content as an HTML file
                with open(f"output/{filename}.html", "w", encoding="utf-8") as file:
                    file.write(article_content)
                print(f"Content saved for {url}")
            else:
                print(f"No article content found in {url}")
        else:
            print(f"Failed to download content from {url}")

if __name__ == "__main__":
    main()
