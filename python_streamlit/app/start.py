import streamlit as st
import json
from config import Config
from openai import AzureOpenAI


class Chat:
    def __init__(self):
        self.system_message = "You are a helpful assistant."
        self.interactions = []


class AppState:
    def __init__(self):
        self.chat_history = [Chat()]
        self.current_chat = self.chat_history[0]
    
    def create_new_chat(self):
        self.current_chat = Chat()
        self.chat_history.append(self.current_chat)
    
    def switch_to_chat(self, index):
        self.current_chat = self.chat_history[index]

    @staticmethod
    def get_state():
        if "state" in st.session_state:
            return st.session_state.state
        else:
            st.session_state.state = AppState()
            return st.session_state.state

def show_chat_msg(cfg, chat) -> None:
    chat_service = ChatService(cfg.azure_openai_api_key, cfg.azure_openai_endpoint, cfg.azure_openai_deployment, chat.interactions, chat.system_message)
    chat_tab, settings_tab = st.tabs(["Chat", "Settings"])
    
    with chat_tab:
        for message in chat_service.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        prompt = st.chat_input("Ask anything")
        if prompt:
            chat_service.chat(prompt)
            st.rerun()
    
    with settings_tab:
        chat.system_message = st.text_area("Settings", height=300, value=chat.system_message)
        st.rerun()

class ChatService:
    def __init__(self, api_key: str, endpoint: str, deployment_name: str, messages, system_msg: str):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-12-01-preview", # Data plane - inference from  https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#data-plane-inference
            azure_endpoint=endpoint
        )
        self.deployment_name = deployment_name
        self.messages = messages
        self.system_msg = system_msg
        self.messages.append({"role": "system", "content": self.system_msg})

    def chat(self, user_message: str):
        self.messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=self.messages
        )

        print(json.dumps(self.messages, indent=2))

        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})

    def clear_chat(self) -> None:
        self.messages.clear()


def start() -> None:
    st.set_page_config(layout="wide")
    cfg = Config()
    
    state = AppState.get_state()
    
    with st.sidebar:
        if st.button("New Chat", key="new_chat_button"):
            state.create_new_chat()
            st.rerun()

        st.title("Menu")
        for i, chat in enumerate(state.chat_history):
            if st.sidebar.button(f"Chat {i+1}", key=f"chat_button_{i}"):
                state.switch_to_chat(i)
                st.rerun()
    
    show_chat_msg(cfg, state.current_chat)

start()