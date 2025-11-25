import requests
import json
import time

def test_anxiety_query():
    url = "http://localhost:8000/api/chat"
    payload = {"message": "Estou sentindo muita ansiedade ultimamente. O que vocês me aconselham?"}
    
    print(f"Sending request to {url}...")
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload, timeout=120) # 2 minute timeout
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Status Code: {response.status_code}")
        print(f"Duration: {duration:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"FAILURE: Unexpected status code. Body: {response.text}")
            
    except Exception as e:
        print(f"FAILURE: Exception occurred: {e}")

if __name__ == "__main__":
    test_anxiety_query()
