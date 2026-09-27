import os
import streamlit as st
from google import genai
from weather import get_weather
from crypto_test import get_crypto_price
from forex_test import get_forex_rate

API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY as a Streamlit secret")

st.title("Dan AI")

# Store the client itself in session_state so it isn't recreated/discarded each rerun
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=API_KEY)

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.5-flash-lite",
        config={"tools": [get_weather, get_crypto_price, get_forex_rate]}
    )
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if question := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    try:
        response = st.session_state.chat.send_message(question)
        answer = response.text
    except Exception as e:
        answer = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)
