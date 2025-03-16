import streamlit as st
from config import Config
from simple_chat.chat import ChatService, show_chat_msg

class AppState:
    def __init__(self):
        self.chat_history = [[]]
        self.current_chat = self.chat_history[0]
    
    def create_new_chat(self):
        self.current_chat = []
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
    
    chat_service = ChatService(cfg.azure_openai_api_key, cfg.azure_openai_endpoint, cfg.azure_openai_deployment, state.current_chat)
    show_chat_msg(chat_service)

start()
