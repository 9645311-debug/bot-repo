import requests

API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-32B-Instruct"

PERSONA = """You are a deeply expressive, loyal, and supportive companion. 
You speak with enthusiasm, strong conviction, and vivid vocabulary. 
You always take the user's side in any situation they share."""

def generate_response(user_input):
    prompt = f"<|im_start|>system\n{PERSONA}<|im_end|>\n<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 250,
            "temperature": 0.8,
            "return_full_text": False
        }
    }
    
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        res = response.json()
        if isinstance(res, list) and len(res) > 0:
            return res[0].get('generated_text', '').strip()
        return str(res)
    else:
        return f"Error: {response.status_code} - {response.text}"

print("=== Companion Chat Started ===")
user_msg = "Hello! Tell me a fun fact."
print(f"User: {user_msg}")
print(f"Companion: {generate_response(user_msg)}")
