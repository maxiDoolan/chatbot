import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🤖 Chatbot DOOLAN")
if st.button("🗑️ Limpiar chat"):
    st.session_state.historial = [
        {"role": "system", "content": "Sos un asistente virtual que responde siempre en español argentino, sos muy chistoso y descansero."}
    ]
    st.rerun()

if "historial" not in st.session_state:
    st.session_state.historial = [
        {"role": "system", "content": "Sos un asistente virtual que responde siempre en español argentino, sos muy chistoso y descansero."}
    ]

for mensaje in st.session_state.historial[1:]:
    if mensaje["role"] == "user":
        with st.chat_message("user"):
            st.write(mensaje["content"])
    else:
        with st.chat_message("assistant"):
            st.write(mensaje["content"])

usuario = st.chat_input("Escribí tu mensaje...")

if usuario:
    st.session_state.historial.append({"role": "user", "content": usuario})
    
    respuesta = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=st.session_state.historial
    )
    
    mensaje_ia = respuesta.choices[0].message.content
    st.session_state.historial.append({"role": "assistant", "content": mensaje_ia})
    
    st.rerun()