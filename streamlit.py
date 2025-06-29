import streamlit as st
import requests
from exception.exceptions import CustomException
import sys
import base64
from typing import List, Dict, Any, Tuple

BASE_URL: str = "http://localhost:8000"  # Backend endpoint

st.set_page_config(
    page_title="📈 Stock Market - Agentic Chatbot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title("📈 Stock Market - Agentic Chatbot")

def img_to_base64(image_path):
    """Convert image to base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        print(f"Error converting image to base64: {str(e)}")
        return None



def upload_files_to_backend(uploaded_files: List[Any]) -> None:
    """
    Uploads files to the backend FastAPI server for ingestion.

    Parameters
    ----------
    uploaded_files : List[Any]
        List of files uploaded by the user.
    """
    files: List[Tuple[str, Tuple[str, bytes, str]]] = []
    for f in uploaded_files:
        file_data = f.read()
        if not file_data:
            continue
        files.append(("files", (getattr(f, "name", "file.pdf"), file_data, f.type)))

    if files:
        try:
            with st.spinner("Uploading and processing files..."):
                response = requests.post(f"{BASE_URL}/upload", files=files)
                if response.status_code == 200:
                    st.success("✅ Files uploaded and processed successfully!")
                else:
                    st.error("❌ Upload failed: " + response.text)
        except Exception as e:
            raise CustomException(e, sys)
    else:
        st.warning("Some files were empty or unreadable.")

def display_chat_history(messages: List[Dict[str, str]]) -> None:
    """
    Displays the chat history in the Streamlit app.

    Parameters
    ----------
    messages : List[Dict[str, str]]
        List of chat messages with roles and content.
    """
    st.header("💬 Chat")
    for chat in messages:
        if chat["role"] == "user":
            st.markdown(f"**🧑 You:** {chat['content']}")
        else:
            st.markdown(f"**🤖 Bot:** {chat['content']}")

def send_message_to_backend(user_input: str) -> None:
    """
    Sends the user's message to the backend and updates the chat history.

    Parameters
    ----------
    user_input : str
        The user's input message.
    """
    try:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Bot is thinking..."):
            payload = {"question": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            st.session_state.messages.append({"role": "bot", "content": answer})
            st.rerun()
        else:
            st.error("❌ Bot failed to respond: " + response.text)
    except Exception as e:
        raise CustomException(e, sys)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar: Upload documents
with st.sidebar:

    img_base64 = img_to_base64("img/icon.png")
    if img_base64:
        st.sidebar.markdown(
        f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
        unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.header("📄 Upload Documents")
    st.markdown("Upload **stock market PDFs or DOCX** to create knowledge base.")
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx"], accept_multiple_files=True)

    if st.button("Upload and Ingest"):
        if uploaded_files:
            upload_files_to_backend(uploaded_files)
    st.sidebar.markdown("---")

# Display chat history
display_chat_history(st.session_state.messages)

# Chat input box at bottom
with st.form(key="chat_form", clear_on_submit=True):
    user_input: str = st.text_input("Your message", placeholder="e.g. Tell me about NIFTY 50")
    submit_button: bool = st.form_submit_button("Send")

if submit_button and user_input.strip():
    send_message_to_backend(user_input)