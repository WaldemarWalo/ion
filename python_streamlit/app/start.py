import streamlit as st
from config import Config
from simple_chat.chat import ChatService, show_chat_msg

def start() -> None:
    st.set_page_config(layout="wide")
    cfg = Config()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_service = ChatService(cfg.azure_openai_api_key, cfg.azure_openai_endpoint, cfg.azure_openai_deployment, st.session_state.messages)
    show_chat_msg(chat_service)

start()
