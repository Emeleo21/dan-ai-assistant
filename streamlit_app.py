import os
import streamlit as st
from google import genai

from weather import get_weather
from crypto_test import get_crypto_price
from forex_test import get_forex_rate
from news_test import get_news
from clock_test import get_local_time
from search_test import web_search

st.set_page_config(page_title="Dan AI", page_icon="🤖", layout="centered")

API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY as a Streamlit secret")

TOOLS = [get_weather, get_crypto_price, get_forex_rate, get_news, get_local_time, web_search]

if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=API_KEY)

def new_chat():
    return st.session_state.client.chats.create(
        model="gemini-3.5-flash-lite",
        config={"tools": TOOLS},
    )

if "chat" not in st.session_state:
    st.session_state.chat = new_chat()
    st.session_state.messages = []

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
    st.caption("Built with Streamlit + Google Gemini. Live data from Open-Meteo, CoinGecko, Twelve Data, Google News and DuckDuckGo.")

# ---------- Chat history ----------
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# ---------- New message ----------
if question := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑"):
        st.write(question)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                answer = st.session_state.chat.send_message(question).text
            except Exception as e:
                answer = f"Error: {e}"
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
