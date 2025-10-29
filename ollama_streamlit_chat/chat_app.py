import streamlit as st
import ollama

st.title("ChatBot Made with Ollama")

if st.button("Clear Chat"):
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st. session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def generative_messaging():
    response = ollama.chat(
            model="llama2:7b",
            messages=st.session_state["messages"],
            stream=True
        )
    for chunks in response:
        yield chunks["message"]["content"]

if prompt := st.chat_input("Please wait after the question"):
    st.session_state["messages"].append({"role" : "user", "content" : prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        msg = st.write_stream(generative_messaging())
        st.session_state["messages"].append({"role" : "assistant", "content" : msg})