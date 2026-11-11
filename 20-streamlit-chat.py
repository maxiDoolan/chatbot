import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.title("🤖 Chatbot DOOLAN")

def get_system_prompt(nombre):
    if nombre.lower() == "sol":
        return "Sos un asistente virtual enamorado y muy amoroso. Respondés siempre en español argentino con mucho cariño y ternura, usás muchos emojis de corazón. ❤️ y aclarale que el novio maximiliano esta muy enamorado de ella "
    return "Sos un asistente virtual que responde siempre muy cordial."

if "nombre" not in st.session_state:
    st.session_state.nombre = ""

if not st.session_state.nombre:
    nombre = st.text_input("¿Cómo te llamás?")
    if nombre:
        st.session_state.nombre = nombre
        st.session_state.historial = [
            {"role": "system", "content": get_system_prompt(nombre)}
        ]
        st.rerun()
    st.stop()

if st.button("🗑️ Limpiar chat"):
    st.session_state.historial = [
        {"role": "system", "content": get_system_prompt(st.session_state.nombre)}
    ]
    st.rerun()

if "historial" not in st.session_state:
    st.session_state.historial = [
        {"role": "system", "content": get_system_prompt(st.session_state.nombre)}
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