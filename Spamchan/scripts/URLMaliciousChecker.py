import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import mimetypes
import base64

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

def download_and_check_files(url, depth=1, directory='downloads'):
    # Main function to recursively obtain HTML, download files, and check them
    malicious_percentage = 0 
    final_url, html = get_final_html(url)
    # print(f"Final URL: {final_url}")

    links = extract_links(html)
    # print(f"Links in HTML: {links}")

    if not os.path.exists(directory):
        os.makedirs(directory)

    if depth > 1:
        # Recursively follow links
        for link in links:
            absolute_link = urljoin(final_url, link)
            
            malicious_percentage += download_and_check_files(absolute_link, depth - 1, directory)
    else:
        # Download files and check them
        for link in links:
            absolute_link = urljoin(final_url, link)
            if not absolute_link.endswith(('.html', '.htm', '/')):
                # If the URL does not point to an HTML file or a directory, download and check it
                
                # malicious_percentage += download_file_and_check(absolute_link, directory)
                result = download_file_and_check(absolute_link, directory)
                if result is not None:
                    malicious_percentage+=result 
    
    return malicious_percentage            

def download_file_and_check(url, directory):
    # Function to download a file and check it using VirusTotal
    filename = url.split('/')[-1]
    filepath = os.path.join(directory, filename)
    os.system(f"curl -o '{filepath}' '{url}'")

    # Check the downloaded file using VirusTotal
    check_result = check_file_with_virustotal(filepath)
    return check_result

def check_file_with_virustotal(filepath):
    url = "https://www.virustotal.com/api/v3/files"
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type is None:
        mime_type = "application/octet-stream"

    files = {"file": (os.path.basename(filepath), open(filepath, "rb"), mime_type)}
    headers = {
        "accept": "application/json",
        "x-apikey": "f02d8b8565e92758edd0e06062538c853ddd914276a74c2a6473a74002c3d8a9"
    }

    response = requests.post(url, files=files, headers=headers)
    response_json = response.json()
    
    try:
        if 'data' in response_json:
            analysis_id = response_json['data']['id']
            decoded_string = base64.b64decode(analysis_id).decode('utf-8')
            split_string = decoded_string.split(":")
            decoded_final = split_string[0]

            url_get_report = f"https://www.virustotal.com/api/v3/files/{decoded_final}"
            headers_get_report = {
                "accept": "application/json",
                "x-apikey": "f02d8b8565e92758edd0e06062538c853ddd914276a74c2a6473a74002c3d8a9"
            }
            response_get_report = requests.get(url_get_report, headers=headers_get_report)
            response_json2 = response_get_report.json()

            if 'data' in response_json2:
                last_analysis_stats = response_json2['data']['attributes']['last_analysis_stats']
                malicious = last_analysis_stats.get('malicious', 0)
                undetected = last_analysis_stats.get('undetected', 0)
                total_detections=0

                # total_detections = malicious + undetected
                if malicious is not None:
                  total_detections += malicious
                if undetected is not None:
                   total_detections += undetected
                if total_detections > 0:
                    malicious_percentage = (malicious / total_detections) * 100
                else:
                    malicious_percentage = 0
                
                print(f"Malicious percentage: {malicious_percentage}%")
                    
                return malicious_percentage    
                # print(f"Report for file {os.path.basename(filepath)}: {last_analysis_stats}")
                
            else:
                print(f"No data found for {os.path.basename(filepath)}")
        else:
            print(f"No data found for {os.path.basename(filepath)}")
    
    except Exception as e:
       print(f"An error occurred: {str(e)}")    
    
if __name__ == "__main__":
    # Replace 'your_link_here' with the actual link you want to start with
    starting_url = 'https://gptzero.stoplight.io/docs/gptzero-api/d2144a785776b-ai-detection-on-single-string'
    download_and_check_files(starting_url, depth=2)