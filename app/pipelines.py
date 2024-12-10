import os
import pickle
import faiss
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from joblib import dump, load
import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings


def text_extraction_pipeline(uploaded_file):
    """
    Extracts text content from a PDF file.

    Args:
        uploaded_file (UploadedFile): The uploaded PDF file.

    Returns:
        str: Extracted text content from the PDF.
    """
    try:
        reader = PdfReader(uploaded_file)
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text()
        return extracted_text
    except Exception as e:
        st.error(f"Error extracting text from {uploaded_file.name}: {e}")
        return ""


def text_processing_pipeline(text):
    """
    Splits extracted text into manageable chunks for embedding.

    Args:
        text (str): The extracted text.

    Returns:
        list: A list of text chunks.
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)
        return chunks
    except Exception as e:
        st.error(f"Error processing text: {e}")
        return []


def vectorization_pipeline(chunks, store_name):
    """
    Creates a vector store from text chunks or loads it if it already exists.

    Args:
        chunks (list): List of text chunks.
        store_name (str): Name for the vector store.

    Returns:
        FAISS: The vector store object.
    """
    try:
        if chunks:
            # Check if a vector store already exists for this store_name
            file_path = f"{store_name}.faiss"
            
            if st.session_state.get("use_existing_store") and os.path.exists(file_path):
                # Load existing vector store
                vector_store = faiss.read_index(file_path)
                st.info(f"Using existing vector store: {file_path}")
            else:
                # Create a new vector store
                embeddings = OpenAIEmbeddings()
                vector_store = FAISS.from_texts(chunks, embeddings)
                
                # Save vector store using FAISS' built-in method
                faiss.write_index(vector_store.index, file_path)
                # st.info(f"Vector store created and saved as {file_path}")
            
            return vector_store
        else:
            st.warning("No chunks available for vectorization.")
            return None
    except Exception as e:
        st.error(f"Error during vectorization: {e}")
        return None



    # try:
    #     if chunks:
    #         # Check if a vector store already exists for this store_name
    #         file_path = f"{store_name}.pkl"
    #         if st.session_state.get("use_existing_store") and file_path:
    #             # Load existing vector store
    #             with open(file_path, "rb") as f:
    #                 vector_store = pickle.load(f)
    #             st.info(f"Using existing vector store: {file_path}")
    #         else:
    #             # Create a new vector store
    #             embeddings = OpenAIEmbeddings()
    #             vector_store = FAISS.from_texts(chunks, embeddings)
    #             with open(file_path, "wb") as f:
    #                 pickle.dump(vector_store, f)
    #             st.info(f"Vector store created and saved as {file_path}")
    #         return vector_store
    #     else:
    #         st.warning("No chunks available for vectorization.")
    #         return None
    # except Exception as e:
    #     st.error(f"Error during vectorization: {e}")
    #     return None