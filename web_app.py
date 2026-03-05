import streamlit as st

from agent import CustomerServiceAgent


st.set_page_config(
    page_title="Customer Service Agent",
    page_icon=":telephone_receiver:",
    layout="centered",
)

st.title("Customer Service Agent")
st.caption("Ask support questions about your platform.")

if "agent" not in st.session_state:
    st.session_state.agent = CustomerServiceAgent()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello. How can I help you today?",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.chat(prompt)
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
