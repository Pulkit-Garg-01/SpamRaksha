# ```python
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_final_html(url):
    # Function to follow redirects and obtain the final HTML content
    response = requests.get(url, allow_redirects=True)
    final_url = response.url
    final_html = response.text
    return final_url, final_html

def extract_links(html):
    # Function to extract links from HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links

def download_file(url, directory):
    # Function to download a file using curl
    filename = url.split('/')[-1]
    filepath = os.path.join(directory, filename)
    os.system(f"curl -o '{filepath}' '{url}'")

def main(url, depth=1, directory='downloads'):
    # Main function to recursively obtain HTML and download files
    final_url, html = get_final_html(url)
    print(f"Final URL: {final_url}")

    links = extract_links(html)
    print(f"Links in HTML: {links}")

    if not os.path.exists(directory):
        os.makedirs(directory)

    if depth > 1:
        # Recursively follow links
        for link in links:
            absolute_link = urljoin(final_url, link)
            main(absolute_link, depth - 1, directory)
    else:
        # Download files
        for link in links:
            absolute_link = urljoin(final_url, link)
            download_file(absolute_link, directory)


# def main(url, depth=1):
#     # Main function to recursively obtain HTML and links
#     final_url, html = get_final_html(url)
#     print(f"Final URL: {final_url}")

#     links = extract_links(html)
#     print(f"Links in HTML: {links}")

#     if depth > 1:
#         # Recursively follow links
#         for link in links:
#             absolute_link = urljoin(final_url, link)
#             main(absolute_link, depth - 1)

if __name__ == "__main__":
    # Replace 'your_link_here' with the actual link you want to start with
    starting_url = 'https://www.google.com'
    main(starting_url, depth=2)

# ```