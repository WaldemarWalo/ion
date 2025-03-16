from openai import AzureOpenAI
import streamlit as st


def show_chat_msg(chat_service) -> None:
    
    st.header("Chat")
    if st.button("New Chat"):
        chat_service.clear_chat()
        st.rerun()

    for message in chat_service.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    prompt = st.chat_input("Ask anything")
    if prompt:
        chat_service.chat(prompt)
        st.rerun()


class ChatService:
    def __init__(self, api_key: str, endpoint: str, deployment_name: str, messages):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-12-01-preview", # Data plane - inference from  https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#data-plane-inference
            azure_endpoint=endpoint
        )
        self.deployment_name = deployment_name
        self.messages = messages

    def chat(self, user_message: str):
        self.messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=self.messages
        )

        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})

    def clear_chat(self) -> None:
        self.messages.clear()
