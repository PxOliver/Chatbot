import streamlit as st
from openai import OpenAI

# Configuración de la página
st.set_page_config(
    page_title="Chatbot Unimodal",
    page_icon="🤖",
    layout="centered"
)

# Título
st.title("🤖 Chatbot Unimodal")
st.write("Chatbot de texto desarrollado con Python, Streamlit y Gemini.")

# Conexión con Gemini
client = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
prompt = st.chat_input("Escribe tu mensaje...")

if prompt:

    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)

    # Guardar mensaje
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):

            try:
                response = client.chat.completions.create(
                    model="gemini-3.6-flash",
                    messages=st.session_state.messages
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                # Guardar respuesta
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error("Ocurrió un error al comunicarse con Gemini.")
                st.code(str(e))