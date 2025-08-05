import streamlit as st
from query_parser import is_valid_news_query, extract_search_query
from news_scraper import get_news
from summarizer import summarize_news  # This uses Ollama Mistral
import os
# Add imports for voice features
try:
    import pyttsx3
    import sounddevice as sd
    from vosk import Model, KaldiRecognizer
    import json
except ImportError:
    pyttsx3 = None
    sd = None
    Model = None
    KaldiRecognizer = None

# App configuration
st.set_page_config(
    page_title="PulseAI: Your Real-Time Company News Chatbot",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto"
)

# App header
st.markdown("""
# 🧠 PulseAI: Your Real-Time Company News Chatbot
""")
st.markdown(
    "Ask for the **latest company news** like:<br>"
    "- <span style='color:#1976d2;'>Get me latest news about Amazon</span><br>"
    "- <span style='color:#1976d2;'>Tell me what happened to GCP yesterday</span><br>",
    unsafe_allow_html=True
)

# Voice chat toggle
voice_chat = st.toggle("🎤 Voice Chat", value=False)

# Speech-to-text input if voice chat is enabled
vosk_model_path = "E:/RAP Chatbot - FINALS/vosk-model-small-en-us-0.15"
user_query = ""  # Always define user_query
if voice_chat and Model and sd:
    st.info("Voice chat is ON. Click 'Start Recording' and speak your query.")
    if 'vosk_model' not in st.session_state:
        st.session_state['vosk_model'] = Model(vosk_model_path)  # Use absolute path
    if st.button("Start Recording"):
        st.write("Listening...")
        duration = 5  # seconds
        fs = 16000
        rec = KaldiRecognizer(st.session_state['vosk_model'], fs)
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        # Calculate decibel level
        import numpy as np
        rms = np.sqrt(np.mean(audio.astype(np.float32) ** 2))
        db = 20 * np.log10(rms + 1e-6)
        st.progress(min(max(int((db + 60) * 100 / 60), 0), 100), text=f"Mic Level: {db:.1f} dB")
        rec.AcceptWaveform(audio.tobytes())
        result = json.loads(rec.Result())
        user_query = result.get('text', '')
        st.write(f"You said: {user_query}")
        if not user_query:
            st.warning("No speech detected. Please try again and speak clearly into the microphone.")
        else:
            st.session_state['auto_get_news'] = True
else:
    user_query = st.text_input("Enter your Query:")

output_style = st.selectbox("Choose Output Style", ["Formal business summary", "Casual conversation", "Quick bullet points"])

# Auto-trigger Get News if flag is set (for voice)
if st.session_state.get('auto_get_news') or st.button("🔍 Get News"):
    st.session_state['auto_get_news'] = False
    if not user_query:
        st.warning("⚠️ Please enter a query.")
    elif not is_valid_news_query(user_query):
        # Handle greetings and small talk
        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        small_talk = [
            ("how are you", "😊 I'm doing well, thank you! How can I help you with the latest company news today?"),
            ("how do you do", "😊 I'm doing great! How can I assist you with company news today?"),
            ("what's up", "Not much! Ready to get you the latest company news. What are you interested in?"),
            ("thank you", "You're welcome! If you need more news, just ask."),
            ("thanks", "You're welcome! Let me know if you need more news.")
        ]
        user_lower = user_query.lower().strip()
        if any(greet in user_lower for greet in greetings):
            st.success("👋 Hello! How can I help you with the latest company news today?")
        elif any(phrase in user_lower for phrase, _ in small_talk):
            for phrase, reply in small_talk:
                if phrase in user_lower:
                    st.info(reply)
                    break
        else:
            st.info("🤖 I'm your Company News Bot! Ask me for the latest news about any company, or just say hi.")
    
    else:
        # Support CSV-style input for multiple companies
        if ',' in user_query:
            company_names = [c.strip().title() for c in user_query.split(',') if c.strip()]
        else:
            # Always extract and validate a single company name
            company_name = extract_search_query(user_query)
            if not company_name:
                st.error("❌ Please enter a valid company name. Only real company names are accepted.")
                st.stop()
            company_names = [company_name]
        for search_term in company_names:
            st.info(f"🔎 Searching for news about: **{search_term}**")
            news_items = get_news(search_term)
            if not news_items:
                st.warning(f"❌ No relevant news found for {search_term}. Try a different company or phrasing.")
                continue
            st.subheader(f"📰 News Sources Found: {search_term}")
            for item in news_items:
                st.markdown(f"- 🔗 [{item['title']}]({item['link']})")
            # Decide summarization mode: broad (company) or specific (person/incident)
            specific_keywords = ["ceo", "incident", "issue", "scandal", "lawsuit", "breach", "hack", "data leak", "fired", "resigned", "death", "accident", "arrest", "investigation"]
            query_lower = user_query.lower()
            is_specific = any(word in query_lower for word in specific_keywords)
            if is_specific:
                combined_text = "\n\n".join([
                    (item.get('text') or open(item['file'], 'r', encoding='utf-8').read() if item.get('file') else '')
                    for item in news_items
                ])
                articles_for_summary = [{
                    'title': f"Combined summary for: {search_term}",
                    'link': '',
                    'text': combined_text
                }]
                st.subheader(f"✍️ AI-Powered Combined Summary: {search_term}")
                summary = summarize_news(articles_for_summary, style=output_style)
                st.success(summary)
            else:
                st.subheader(f"✍️ AI-Powered Summaries (Per Article): {search_term}")
                for item in news_items:
                    article_text = item.get('text', '')
                    if not article_text and item.get('file'):
                        try:
                            with open(item['file'], 'r', encoding='utf-8') as f:
                                article_text = f.read()
                        except Exception:
                            article_text = ''
                    if article_text:
                        summary = summarize_news([{'title': item['title'], 'link': item['link'], 'text': article_text}], style=output_style)
                        st.info(f"**Summary:** {summary}")
                    else:
                        st.info("No article content available for summarization.")
                    if item.get('file') and os.path.exists(item['file']):
                        os.remove(item['file'])
    # After generating the reply (e.g., summary or chatbot message):
    if voice_chat and pyttsx3:
        engine = pyttsx3.init()
        # Speak the last summary or info message
        try:
            if 'summary' in locals():
                engine.say(summary)
            elif 'reply' in locals():
                engine.say(reply)
            engine.runAndWait()
        except Exception:
            pass

# To speed up: reduce number of articles, use a smaller LLM, or upgrade hardware. See code comments for details.
