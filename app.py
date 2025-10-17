from flask import Flask, render_template, request, jsonify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

app = Flask(__name__)

sia = SentimentIntensityAnalyzer()

# Store conversations {topic: [messages]}
conversations = {}

def determine_topic(message):
    """Basic topic categorization based on keywords."""
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

    # Sentiment-based responses
    if sentiment['compound'] <= -0.5:
        reply = "I can see that you're feeling sad 😔. Try not to worry too much. Remember, I'm here to listen. 💌"
    elif sentiment['compound'] >= 0.5:
        reply = "You sound happy! Keep smiling 😄"
    else:
        reply = "I understand. Thanks for sharing. 💖"

    # Emotion-aware adjustments
    if "joke" in msg_lower or "funny" in msg_lower:
        reply = "Why did the computer go to the doctor? Because it caught a virus! 😆"

    if "how are you" in msg_lower:
        reply = "I'm doing great! How about you?"

    if "name" in msg_lower:
        reply = "My name is Pinky! 💖"

    if any(word in msg_lower for word in ["advice", "help", "support"]):
        reply = "Always be yourself and stay positive! 🌟"

    if any(word in msg_lower for word in ["love", "breakup", "boyfriend", "girlfriend"]):
        if sentiment['compound'] <= -0.5:
            reply = "I can see this is hard for you 💔. Take your time to heal. I'm here for you."

    return reply

@app.route("/")
def index():
    topics = list(conversations.keys())
    return render_template("index.html", topics=topics)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    topic = determine_topic(message)

    bot_reply = get_bot_response(message)

    if topic not in conversations:
        conversations[topic] = []
    conversations[topic].append({"user": message, "bot": bot_reply})

    return jsonify({"reply": bot_reply, "topic": topic})

@app.route("/history/<topic>")
def history(topic):
    chat_history = conversations.get(topic, [])
    return jsonify({"history": chat_history})

if __name__ == "__main__":
    app.run(debug=True)





