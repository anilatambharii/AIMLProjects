import requests

url = "http://127.0.0.1:8000/analyze"
data = {"text": "I loved this product! It exceeded my expectations."}

response = requests.post(url, json=data)

# Print the response (predicted category)
print(data)
print(response.json())
