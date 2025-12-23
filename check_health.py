import requests
import sys

try:
    print("Sending GET request to http://127.0.0.1:8000/register ...")
    response = requests.get("http://127.0.0.1:8000/register")
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.text)
except Exception as e:
    print(f"Request Failed: {e}")
