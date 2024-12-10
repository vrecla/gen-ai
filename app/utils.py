import os
import streamlit as st
import json
from dotenv import load_dotenv
    

def load_api_key():
    """
    Loads the OpenAI API key from environment variables.
    
    Returns:
        str: The OpenAI API key.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("API key not found. Please set OPENAI_API_KEY in your environment variables.")
    return api_key


def initialize_history():
    """
    Initializes an empty chat history if not already present in the session state.
    
    Returns:
        list: An empty chat history.
    """
    if "history" not in st.session_state:
        st.session_state.history = []
    return st.session_state.history


def save_history(history):
    """
    Saves the chat history to a local JSON file.
    
    Args:
        history (list): A list of dictionaries containing chat history.
    """
    try:
        with open("chat_history.json", "w") as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        st.error(f"Error saving history: {e}")


def load_history():
    """
    Loads the chat history from a local JSON file.
    
    Returns:
        list: A list of dictionaries containing chat history.
    """
    if os.path.exists("chat_history.json"):
        try:
            with open("chat_history.json", "r") as f:
                history = json.load(f)
            return history
        except Exception as e:
            st.error(f"Error loading history: {e}")
            return []
    else:
        return initialize_history()


def clear_history():
    """
    Clears the chat history from both session state and local storage.
    """
    st.session_state.history = []
    if os.path.exists("chat_history.json"):
        try:
            os.remove("chat_history.json")
        except Exception as e:
            st.error(f"Error clearing history: {e}")


def display_chat_history():
    """
    Displays the current chat history in the Streamlit app.
    """
    if "history" in st.session_state and st.session_state.history:
        st.markdown("### Chat History")
        for chat in st.session_state.history:
            st.write(f"**You:** {chat['query']}")
            st.write(f"**Bot:** {chat['response']}")


def validate_uploaded_files(files):
    """
    Validates the uploaded files for type and size.
    
    Args:
        files (list): List of uploaded files.

    Returns:
        bool: True if all files are valid, False otherwise.
    """
    max_file_size_mb = 10  # Set a max file size (e.g., 10MB per file)
    for file in files:
        if file.size > max_file_size_mb * 1024 * 1024:
            st.error(f"File {file.name} exceeds the maximum allowed size of {max_file_size_mb}MB.")
            return False
        if not file.name.endswith(".pdf"):
            st.error(f"File {file.name} is not a valid PDF.")
            return False
    return True