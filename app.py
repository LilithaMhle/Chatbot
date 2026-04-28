from flask import Flask, render_template, request, jsonify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download required NLTK data (safe on deploy)
nltk.download('vader_lexicon')

app = Flask(__name__)

sia = SentimentIntensityAnalyzer()

# Store conversations
conversations = {}

def determine_topic(message):
    msg = message.lower()

    if any(word in msg for word in ["exam", "test", "homework", "study"]):
        return "Exam Stress"
    if any(word in msg for word in ["hello", "hi", "hey"]):
        return "Greeting"
    if any(word in msg for word in ["love", "boyfriend", "girlfriend", "relationship", "breakup"]):
        return "Relationship"
    if any(word in msg for word in ["funny", "joke", "laugh"]):
        return "Humor"
    if any(word in msg for word in ["advice", "help", "support"]):
        return "Advice"

    return "General"


def get_bot_response(message):
    sentiment = sia.polarity_scores(message)
    msg_lower = message.lower()

    if sentiment["compound"] <= -0.5:
        reply = "I can see you're feeling down 😔. I'm here for you 💙"
    elif sentiment["compound"] >= 0.5:
        reply = "You sound happy 😄 Keep it up!"
    else:
        reply = "I understand. Tell me more 💬"

    if "joke" in msg_lower:
        reply = "Why did the computer go to therapy? It had too many bytes 😆"

    if "how are you" in msg_lower:
        reply = "I'm doing great! How about you?"

    if "name" in msg_lower:
        reply = "I'm Pinky 💖 your AI chatbot"

    if "advice" in msg_lower or "help" in msg_lower:
        reply = "Stay consistent and believe in yourself 🌟"

    if any(word in msg_lower for word in ["love", "breakup", "relationship"]):
        if sentiment["compound"] <= -0.5:
            reply = "I know this is tough 💔 Take your time to heal."

    return reply


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    topic = determine_topic(message)
    bot_reply = get_bot_response(message)

    if topic not in conversations:
        conversations[topic] = []

    conversations[topic].append({
        "user": message,
        "bot": bot_reply
    })

    return jsonify({
        "reply": bot_reply,
        "topic": topic
    })


@app.route("/history/<topic>")
def history(topic):
    return jsonify(conversations.get(topic, []))


# IMPORTANT for Render/Gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)





