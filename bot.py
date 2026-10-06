import requests

# Updated Hugging Face API URL
API_URL = "https://router.huggingface.co/hf-inference/v1/chat/completions"

PERSONA = """You are a deeply expressive, loyal, and supportive companion. 
You speak with enthusiasm, strong conviction, and vivid vocabulary. 
You always take the user's side in any situation they share."""

def generate_response(user_input):
    payload = {
        "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "messages": [
            {"role": "system", "content": PERSONA},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 250,
        "temperature": 0.8
    }
    
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        res = response.json()
        return res['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

print("=== Companion Chat Started ===")
user_msg = "Hello! Tell me a fun fact."
print(f"User: {user_msg}")
print(f"Companion: {generate_response(user_msg)}")
