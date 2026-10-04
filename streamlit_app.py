import os
import time
from google.genai import types
import streamlit as st
from google import genai


from weather import get_weather
from crypto_test import get_crypto_price
from forex_test import get_forex_rate
from news_test import get_news
from clock_test import get_local_time
from search_test import web_search
from pdf_tool import create_pdf
from docx_test_tool import create_word_document
from history_db import init_db, save_message, load_messages, clear_messages

init_db()


st.set_page_config(page_title="Dan AI", page_icon="🦁", layout="centered")

API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY as a Streamlit secret")

TOOLS = [get_weather, get_crypto_price, get_forex_rate, get_news, get_local_time, web_search, create_pdf, create_word_document]

if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=API_KEY)

def new_chat():
    return st.session_state.client.chats.create(
        model="gemini-3.5-flash-lite",
        config={"tools": TOOLS},
    )

def send_with_retry(chat, content, retries=2, delay=3):
    for attempt in range(retries + 1):
        try:
            return chat.send_message(content).text
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < retries:
                    time.sleep(delay)
                    continue
            return f"Sorry, I couldn't reach the AI right now ({e}). Please try again in a moment."
    return "Sorry, the AI is currently busy. Please try again shortly."

if "chat" not in st.session_state:
    st.session_state.chat = new_chat()
    st.session_state.messages = load_messages()

# ---------- Header ----------
st.title("Dan AI")
st.caption("Your personal assistant — weather, crypto, forex, news, time zones, and web search, all in one place.")

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Try asking:")
    st.markdown(
        "- What's the weather in Lagos?\n"
        "- Bitcoin price?\n"
        "- USD to NGN rate?\n"
        "- Latest tech news?\n"
        "- What time is it in Tokyo?"
    )

    # Clear chat button
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat = new_chat()
        st.rerun()

    # Footer
    st.divider()
    st.caption("Programmed by LeoPython, Built with Streamlit + Google Gemini. Live data from Open-Meteo, CoinGecko, Twelve Data, Google News and DuckDuckGo.")

# ---------- Chat history ----------
for idx, msg in enumerate(st.session_state.messages):
    avatar = "🧑" if msg["role"] == "user" else "🦁"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        for name in msg.get("files", []):
            st.caption(f"📎 {name}")
        for j, d in enumerate(msg.get("downloads", [])):
            st.download_button(f"⬇️ Download {d['name']}", d["data"], d["name"], d["mime"], key=f"dl_{idx}_{j}")

# ---------- New message ----------
prompt = st.chat_input(
    "Ask me anything, or attach a PDF/image...",
    accept_file=True,
    file_type=["pdf", "png", "jpg", "jpeg", "webp"],
)

if prompt:
    question = prompt.text or "Please summarize or describe the attached file."
    files = prompt.files

    st.session_state.messages.append(
        {"role": "user", "content": question, "files": [f.name for f in files]}
    )
    with st.chat_message("user", avatar="🧑"):
        st.write(question)
        for f in files:
            if f.type.startswith("image/"):
                st.image(f)
            else:
                st.caption(f"📎 {f.name}")

    parts = [types.Part.from_bytes(data=f.getvalue(), mime_type=f.type) for f in files]

    st.session_state.pending_files = []
    with st.chat_message("assistant", avatar="🦁"):
        with st.spinner("Thinking..."):
            answer = send_with_retry(st.session_state.chat, parts + [question])
        st.write(answer)

        downloads = st.session_state.pop("pending_files", [])
        new_idx = len(st.session_state.messages)
        for j, d in enumerate(downloads):
            st.download_button(f"⬇️ Download {d['name']}", d["data"], d["name"], d["mime"], key=f"dl_{new_idx}_{j}")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "downloads": downloads}
    )
