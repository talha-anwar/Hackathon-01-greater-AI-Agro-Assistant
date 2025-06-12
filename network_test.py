import os
import requests

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("OPENAI_API_KEY not set in environment variables")
    exit(1)

headers = {
    "Authorization": f"Bearer {api_key}"
}

response = requests.get("https://api.openai.com/v1/models", headers=headers)
print(response.status_code)
print(response.text)
