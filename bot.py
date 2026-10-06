@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    payload = {
        "model": "mistral",  # Updated model to avoid 402 payment/rate limits
        "messages": [
            {"role": "system", "content": PERSONA},
            {"role": "user", "content": user_input}
        ]
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            res = response.json()
            answer = res['choices'][0]['message']['content'].strip()
        else:
            answer = f"Error: {response.status_code}"
    except Exception as e:
        answer = f"Error connecting to API: {e}"

    return jsonify({"response": answer})
