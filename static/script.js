let userName = "";
let currentTopic = "General";

// Set user name
function setName() {
  const nameInput = document.getElementById("userName").value.trim();
  if (nameInput) {
    userName = nameInput;
    document.querySelector(".name-input").style.display = "none";
    document.getElementById("chatUser").textContent = `Talking to: ${userName}`;
    addMessage("bot", `Hi ${userName}! 👋 I'm your personal friend, Pinky.`);
  }
}

// Add chat bubble
function addMessage(sender, text) {
  const chatBox = document.getElementById("chatBox");
  const msg = document.createElement("div");
  msg.className = sender === "user" ? "user-msg" : "bot-msg";
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Get selected response mode
function getMode() {
  const radios = document.getElementsByName("mode");
  for (let r of radios) {
    if (r.checked) return r.value;
  }
  return "text";
}

// Send user message
async function sendMessage() {
  const input = document.getElementById("userInput");
  const text = input.value.trim();
  if (!text) return;

  addMessage("user", text);
  input.value = "";
  addMessage("bot", "🤖 Thinking...");

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await response.json();
    const botReply = data.reply;
    currentTopic = data.topic;

    document.querySelector(".bot-msg:last-child").remove();

    addMessage("bot", botReply);

    // Update sidebar with topic
    const topicList = document.getElementById("topicList");
    if (![...topicList.children].some(li => li.textContent === currentTopic)) {
      const li = document.createElement("li");
      li.textContent = currentTopic;
      li.onclick = () => loadTopic(currentTopic);
      topicList.appendChild(li);
    }

    // If voice
    if (getMode() === "voice") {
      const utter = new SpeechSynthesisUtterance(botReply);
      utter.lang = "en-US";
      speechSynthesis.speak(utter);
    }
  } catch (err) {
    document.querySelector(".bot-msg:last-child").textContent =
      "⚠️ Sorry, I couldn't connect to the AI right now.";
  }
}

// Voice input from mic
function startVoice() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert("Your browser doesn’t support speech recognition.");
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.start();

  addMessage("bot", "🎤 Listening...");

  recognition.onresult = function (event) {
    const voiceText = event.results[0][0].transcript;
    document.getElementById("userInput").value = voiceText;
    sendMessage();
  };
}

// Load chat history for a topic
async function loadTopic(topic) {
  currentTopic = topic;
  const chatBox = document.getElementById("chatBox");
  chatBox.innerHTML = "";

  const response = await fetch(`/history/${topic}`);
  const data = await response.json();
  const history = data.history;

  history.forEach(msg => {
    addMessage("bot", msg.bot);
    addMessage("user", msg.user);
  });
}





