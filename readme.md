# 🧠 PulseAI: Your Real-Time Company News Chatbot
_Built for Rapid Acceleration Partners Pvt. Ltd._

---

## 📌 Overview

PulseAI is a user-friendly, real-time company news chatbot that fetches and summarizes the latest news from the web using scraping tools, open AI models running locally, and optional voice interaction.

Executives, analysts, and techies can simply type or say their question — PulseAI instantly delivers clear, actionable news summaries with direct links.

- 🧑‍💻 **No coding required**
- 🎙 **Voice-enabled user queries supported**
- ✨ **Just launch, ask, and get results — instantly!**

---

## 🚀 Key Features

| Feature                     | Details                                                                  |
|-----------------------------|--------------------------------------------------------------------------|
| 💬 Natural Language Input    | Ask in plain English (e.g., “What’s the latest news on Microsoft?”)      |
| 🎙 Voice Input               | Speak your query using your microphone (via Vosk)                        |
| 📊 Multiple Companies        | Ask about more than one: `amazon, google, tcs`                           |
| 👤 Incident Detection        | Ask about incidents: “What happened to the CEO of Apple?”                |
| 🤝 Friendly Chat             | Responds to greetings and simple small talk                              |
| 🌐 Web Scraping              | Fetches news via Bing, BeautifulSoup, newspaper3k, trafilatura           |
| 🧠 Local AI Summarization    | Summarizes articles via Mistral 7B model offline using Ollama            |
| 🖥️ Streamlit UI              | Clean, interactive web interface — no code needed                        |

---

## 🛠 Tools & Libraries Used

- Python 3.8+
- Streamlit
- `requests`, `beautifulsoup4`, `newspaper3k`, `trafilatura`
- Vosk (for voice input)
- Ollama (self-hosted model server)
- Mistral 7B (open LLM for all summarization)

---

## 💻 Installation Guide

### 1️⃣ Clone the Repository

git clone https://github.com/SajivJess/RAP-Hackathon.git
cd RAP-Hackathon

text

Or download the ZIP from GitHub and extract.

---

### 2️⃣ Set Up Python Environment

- **Install Python 3.8+** from [python.org](https://python.org)
- **Create a virtual environment:**

  - Windows:
    ```
    python -m venv venv
    venv\Scripts\activate
    ```
  - macOS/Linux:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

- **Install the dependencies:**

    ```
    pip install -r requirements.txt
    ```

  If requirements.txt is missing, install manually:
    ```
    pip install streamlit requests beautifulsoup4 newspaper3k trafilatura vosk
    ```

  For voice:
    - **Windows:**
      ```
      pip install pyaudio
      ```
    - **macOS/Linux**: First install portaudio via brew/apt/yum, then:
      ```
      pip install pyaudio
      ```

---

### 3️⃣ Install Ollama & Pull Mistral Model

- [Download Ollama](https://ollama.com/download) for Windows/macOS/Linux
- **Launch the Ollama server**:
ollama serve

text
- **In a new terminal, pull the Mistral model:**
ollama pull mistral

text

---

### 4️⃣ Launch PulseAI

streamlit run app.py

text

Open your browser to: [http://localhost:8501](http://localhost:8501)

---

## 🧠 How Does PulseAI Work?

1. **Input** – Type or speak a query like “What’s new with OpenAI?” or “Show Amazon layoffs news.”
2. **Web Search** – Finds breaking news via Bing and custom scraping (no paid APIs).
3. **Scraping** – Extracts article text using advanced techniques; skips junk or paywalled content automatically.
4. **Summarization** – Sends article content + your chosen output style to the local Mistral 7B LLM.
5. **Output** – Shows news links AND AI-powered summary, in your selected style (formal, bullet, casual, etc).

---

## 🎤 Using Voice Feature

- Ensure your mic works.
- Toggle voice chat “ON” or use the microphone feature in the app.
- Speak your question clearly.
- The result is shown and optionally read back aloud.

---

## 🛟 Troubleshooting

| Problem                     | Solution                                                |
|-----------------------------|--------------------------------------------------------|
| ❌ Ollama not running        | Run `ollama serve` and ensure Mistral is pulled        |
| ❌ Missing libraries         | Run `pip install -r requirements.txt` again            |
| ⚠️ News webpage not scraping | Some sites block bots — PulseAI will skip or warn      |
| 🎙 Mic not detected          | Check permissions, and that PyAudio/Vosk installed     |

---

## 🧩 Project Structure

RAP-Hackathon/
├── app.py # Main Streamlit app
├── summarizer.py # AI summarization logic
├── news_scraper.py # News scraping and extraction functions
├── voice_input.py # Voice recognition (if present)
├── query_parser.py # Query intent and extraction
├── typo_check.py # Typos and spelling correction
├── utils.py # Helper utilities
├── requirements.txt # Python requirements
└── README.md # This file!

text

---

## 🙋 Example Usage

| Action                          | Example                                 |
|----------------------------------|-----------------------------------------|
| 🗣 Ask a news question           | “Get me the latest news about Amazon”   |
| 🏢 Ask about multiple companies  | “amazon, tcs, google”                   |
| 👨‍💼 Ask about a CEO/incident      | “What happened to the CEO of Infosys?”  |
| 👋 Greet the bot                 | “Hi”, “How are you?”, “Good morning”    |
| 📝 Change summary style          | Use the “Output Style” dropdown         |
| 🎙 Use voice query               | Speak after enabling voice in the UI    |

---

## 📢 Credits

- Developed by Sajiv Jess & Shri Dharshini for Rapid Acceleration Partners Pvt. Ltd.
- Powered by [Mistral 7B](https://mistral.ai/)
- Voice via [Vosk](https://alphacephei.com/vosk/)
- UI: [Streamlit](https://streamlit.io/)

---

🎉 **Get Started with PulseAI Today!**  
Stay informed. Stay ahead.  
**PulseAI** – Your Real-Time Company News Chatbot

---

[GitHub Repo](https://github.com/SajivJess/RAP-Hackathon)
