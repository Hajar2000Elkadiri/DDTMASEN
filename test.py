import streamlit as st
import ollama

st.title("💬 ChatDDTM à votre service")

# Initialize message history in session state if not already present
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Comment je peux vous aider?"}]

## Generator for Streaming Tokens
def generate_response():
    response = ollama.chat(model='llama3', stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state.full_message += token
        yield token

# Initialize full message in session state if not already present
if 'full_message' not in st.session_state:
    st.session_state.full_message = ""

# Write message history
if 'messages' in st.session_state:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
        else:
            st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

# Get user input and generate response
user_prompt = st.chat_input("Comment je peux vous aider ? Appuyez sur Entrée pour envoyer.")
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user", avatar="🧑‍💻").write(user_prompt)
    st.session_state.full_message = ""  # Reset full message
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response())
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.full_message})
