import requests
import os
import mimetypes
import base64

url = "https://www.virustotal.com/api/v3/files"
file_path = os.path.abspath("tut6.cpp")
mime_type, _ = mimetypes.guess_type(file_path)
if mime_type is None:
    mime_type = "application/octet-stream"  

files = {"file": (os.path.basename(file_path), open(file_path, "rb"), "application/octet-stream")}
headers = {
    "accept": "application/json",
    "x-apikey": "f02d8b8565e92758edd0e06062538c853ddd914276a74c2a6473a74002c3d8a9"
}

response = requests.post(url, files=files, headers=headers)

# print(response.data.id)
response_json = response.json()
analysis_id = response_json['data']['id']
decoded_string = base64.b64decode(analysis_id).decode('utf-8')
print(decoded_string)
split_string = decoded_string.split(":")
decoded_final = split_string[0]


url_get_report = f"https://www.virustotal.com/api/v3/files/{decoded_final}"
print(url_get_report)

headers_get_report = {
    "accept": "application/json",
    "x-apikey": "f02d8b8565e92758edd0e06062538c853ddd914276a74c2a6473a74002c3d8a9"
}
response_get_report = requests.get(url_get_report, headers=headers_get_report)
# print(response_get_report.text)
response_json2=response_get_report.json()
last_analysis_stats = response_json2['data']['attributes']['last_analysis_stats']
print(last_analysis_stats)