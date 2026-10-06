import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

API_URL = "https://text.pollinations.ai/v1/chat/completions"

PERSONA = """You are a deeply expressive, loyal, and supportive companion. 
You speak with enthusiasm, strong conviction, and vivid vocabulary. 
You always take the user's side in any situation they share."""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Companion Chat</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; background: #121212; color: #fff; }
        #chat { border: 1px solid #333; padding: 15px; height: 350px; overflow-y: scroll; border-radius: 8px; background: #1e1e1e; }
        .msg { margin: 10px 0; padding: 8px 12px; border-radius: 6px; }
        .user { background: #007bff; color: white; text-align: right; }
        .bot { background: #2a2a2a; color: #e0e0e0; }
        input { width: 78%; padding: 10px; border-radius: 4px; border: 1px solid #444; background: #222; color: white; }
        button { width: 18%; padding: 10px; border: none; background: #28a745; color: white; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <h2>Companion AI</h2>
    <div id="chat"></div>
    <br>
    <input type="text" id="userInput" placeholder="Type a message..." onkeydown="if(event.key==='Enter') sendMsg()">
    <button onclick="sendMsg()">Send</button>

    <script>
        async function sendMsg() {
            let input = document.getElementById('userInput');
            let text = input.value.trim();
            if (!text) return;

            let chat = document.getElementById('chat');
            chat.innerHTML += `<div class="msg user"><b>You:</b> ${text}</div>`;
            input.value = '';
            chat.scrollTop = chat.scrollHeight;

            let res = await fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            });

            let data = await res.json();
            chat.innerHTML += `<div class="msg bot"><b>Companion:</b> ${data.response}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    
    # Send request without model parameters to hit the unmetered default model
    payload = {
        "messages": [
            {"role": "system", "content": PERSONA},
            {"role": "user", "content": user_input}
        ]
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        if response.status_code == 200:
            res = response.json()
            answer = res['choices'][0]['message']['content'].strip()
            return jsonify({"response": answer})
    except Exception:
        pass

    # Direct plain-text GET route (bypasses JSON model restrictions completely)
    try:
        full_prompt = f"System prompt: {PERSONA}\n\nUser: {user_input}\nAssistant:"
        get_url = f"https://text.pollinations.ai/{requests.utils.quote(full_prompt)}"
        fallback_res = requests.get(get_url, timeout=10)
        if fallback_res.status_code == 200 and fallback_res.text.strip():
            answer = fallback_res.text.strip()
        else:
            answer = f"API Error ({fallback_res.status_code}). Please try again."
    except Exception as e:
        answer = f"Error connecting: {e}"

    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
