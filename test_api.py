import requests
import json

# Test case categorization
def test_case_categorization():
    url = "http://localhost:8000/categorize-case"
    data = {
        "case_description": "A company failed to deliver goods as per the contract terms",
        "language": "en"
    }
    
    print("\nSending POST request to /categorize-case")
    print("Request data:", json.dumps(data, indent=2))
    
    response = requests.post(url, json=data)
    
    print("\nResponse status code:", response.status_code)
    print("Response data:", json.dumps(response.json(), indent=2))

# Test health check
def test_health():
    url = "http://localhost:8000/health"
    
    print("\nSending GET request to /health")
    response = requests.get(url)
    
    print("Response status code:", response.status_code)
    print("Response data:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_health()
    test_case_categorization() 