from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    model = "llama3.2"  # Replace with your model if different

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    # Tell Ollama NOT to stream output (returns complete JSON)
    response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=60)

    full_reply = ""

    try:
        for line in response.iter_lines():
            if line:
                json_data = json.loads(line.decode("utf-8"))
                content = json_data.get("message", {}).get("content", "")
                full_reply += content
    except Exception as e:
        print("Streaming Parse Error:", e)
        return jsonify({"response": "Sorry, failed to parse streamed response."})

    return jsonify({"response": full_reply})
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
