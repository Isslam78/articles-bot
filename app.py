from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ===== PUT YOUR INFO HERE =====
ACCESS_TOKEN = "PUT_YOUR_TOKEN_HERE"
PHONE_NUMBER_ID = "1525789113940519"
VERIFY_TOKEN = "articles123"
# ==============================

WHATSAPP_URL = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"

# Your articles list
ARTICLES = {
    "1": "📰 Article 1: How to start your project\nhttps://example.com/article1",
    "2": "📰 Article 2: 5 ways to earn money online\nhttps://example.com/article2",
    "3": "📰 Article 3: What is Artificial Intelligence?\nhttps://example.com/article3",
}

def send_message(to, text):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    r = requests.post(WHATSAPP_URL, headers=headers, json=data)
    print(r.text)
    return r

@app.route("/", methods=["GET"])
def home():
    return "Bot is working ✅"

# This verifies the webhook with Meta
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Wrong token", 403

# This receives messages
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(data)
    try:
        entry = data["entry"][0]["changes"][0]["value"]
        if "messages" in entry:
            msg = entry["messages"][0]
            from_number = msg["from"]
            text = msg["text"]["body"].strip().lower()

            if text in ["salam", "hi", "hello", "مرحبا", "سلام"]:
                send_message(from_number, "Hello! 👋\nWant an article? Send me a number:\n\n1 - How to start your project\n2 - Earn money online\n3 - Artificial Intelligence\n\nOr send 'article' to get the full list")

            elif text in ["article", "articles", "مقال", "1", "2", "3"]:
                if text in ["article", "articles", "مقال"]:
                    reply = "Here are our articles:\n\n1 - How to start your project\n2 - Earn money online\n3 - Artificial Intelligence\n\nSend me the number of the article you want"
                    send_message(from_number, reply)
                else:
                    send_message(from_number, ARTICLES.get(text, "I didn't find this article"))

            else:
                send_message(from_number, "I didn't understand 🤔\nSend 'article' to get the articles")
    except Exception as e:
        print("Error:", e)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)