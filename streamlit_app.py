import os
import streamlit as st

st.set_page_config(
    page_title="Dan AI",
    page_icon="🤖",
    layout="centered",
)
from google import genai
from weather import get_weather
from crypto_test import get_crypto_price
from forex_test import get_forex_rate
from news_test import get_news
from clock_test import get_local_time
from search_test import web_search

API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY as a Streamlit secret")

st.title("Dan AI")
st.caption("Your personal assistant — weather, crypto, forex, news, time zones, and web search, all in one place.")
with st.sidebar:
    st.header("Try asking:")
    st.markdown("- What's the weather in Lagos?\n- Bitcoin price?\n- USD to NGN rate?\n- Latest tech news?\n- What time is it in Tokyo?")

# Store the client itself in session_state so it isn't recreated/discarded each rerun
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=API_KEY)

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.5-flash-lite",
        config={"tools": [get_weather, get_crypto_price, get_forex_rate, get_news, get_local_time, web_search]}
    )
    st.session_state.messages = []

for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

if question := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑"):
        st.write(question)

    try:
        response = st.session_state.chat.send_message(question)
        answer = response.text
    except Exception as e:
        answer = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant", avatar="🤖"):
     st.write(answer)
