import requests
import json
import sys

def test_chat():
    url = "http://localhost:8000/api/chat"
    payload = {"message": "Olá, quem são vocês?"}
    
    try:
        print(f"Sending request to {url}...")
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if "response" in data and "session_id" in data:
                print("SUCCESS: API returned expected fields.")
            else:
                print("FAILURE: API missing expected fields.")
                sys.exit(1)
        else:
            print(f"FAILURE: Unexpected status code. Body: {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"FAILURE: Exception occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_chat()
