import streamlit as st
from langchain.llms import OpenAI 
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from app.pipelines import (
    text_extraction_pipeline,
    text_processing_pipeline,
    vectorization_pipeline,
)

from app.utils import load_api_key, initialize_history, save_history, load_history
from app.prompts import generate_prompt
import os


def display_sidebar():
    """Renders the sidebar with app information and controls."""
    with st.sidebar:
        st.title('PDFQuery')
        st.markdown('''
        ## About
        This application is an LLM-powered chatbot built using:
        - [Streamlit](https://streamlit.io/)
        - [LangChain](https://python.langchain.com/)
        - [OpenAI](https://platform.openai.com/docs/models) LLM model
        ''')

        st.markdown("### LLM Model Parameters")
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        max_tokens = st.number_input("Max Tokens", min_value=100, max_value=4000, value=1500)
        st.markdown("""
        <style>
        .footer {
            position: fixed;
            bottom: 10px;
            width: 100%;
            text-align: left;
            font-size: 14px;
            color: #777;
        }
        </style>
        <div class="footer">Created by Vanessa A. Recla</div>
        """, unsafe_allow_html=True)

        return temperature, max_tokens
    
def process_documents(uploaded_files):
    """
    Processes multiple PDF files and returns a combined vector store.
    
    Args:
        uploaded_files (List[UploadedFile]): List of uploaded PDF files.

    Returns:
        FAISS: Combined vector store for all documents.
    """
    combined_chunks = []
    for file in uploaded_files:
        st.info(f"Processing file: {file.name}")
        text = text_extraction_pipeline(file)
        chunks = text_processing_pipeline(text)
        combined_chunks.extend(chunks)

    # Create a single vector store from combined chunks
    vector_store = vectorization_pipeline(combined_chunks, "combined_documents")
    return vector_store


def main():
    """Main function to run the Streamlit app."""
    st.header("Chat with PDFQuery")

    # Sidebar parameters
    temperature, max_tokens = display_sidebar()

    # File uploader for PDFs
    st.markdown("### Upload Documents")
    uploaded_files = st.file_uploader("Upload PDFs", type='pdf', accept_multiple_files=True)

    # Load API Key
    api_key = load_api_key()

    if uploaded_files:
        # Process uploaded documents
        vector_store = process_documents(uploaded_files)

        # Initialize LLM with user-defined parameters
        llm = OpenAI(model_name="gpt-3.5-turbo", temperature=temperature, max_tokens=max_tokens)

        # Load or initialize chat history
        if "history" not in st.session_state:
            st.session_state.history = []

        # Initialize session state for the most recent response
        if "latest_response" not in st.session_state:
            st.session_state.latest_response = ""

        # Input box at the top
        user_query = st.text_input("Enter your question:", key="query_input")

        if user_query:
            # Retrieve context from vector store
            docs = vector_store.similarity_search(query=user_query, k=3)
            document_context = " ".join([doc.page_content for doc in docs])

            # Ensure document context is not empty
            if not document_context:
                response = "No relevant texts found for your query."
            else:
                # Generate a prompt and get a response from LLM
                prompt = generate_prompt(document_context, user_query, st.session_state.history)
                response = llm(prompt)

            # Display the response immediately below the input box
            st.session_state.latest_response = response

            # Add to history (most recent at the top)
            st.session_state.history.insert(0, {"query": user_query, "response": response})

        # Display the most recent response (if available)
        if st.session_state.latest_response:
            st.markdown("---")
            st.write(f"**PDFQuery:** {st.session_state.latest_response}")
            st.markdown("---")

        # Display chat history below the input box
        if st.session_state.history:
            st.subheader("Chat History")
            for chat in st.session_state.history:
                st.write(f"**You:** {chat['query']}")
                st.write(f"**PDFQuery:** {chat['response']}")

    else:
        st.info("Please upload one or more PDF files to start.")

if __name__ == '__main__':
    main()