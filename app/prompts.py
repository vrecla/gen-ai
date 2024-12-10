def generate_prompt(document_context, query, chat_history=None):
    """
    Creates an advanced prompt based on the query type and document context.

    Args:
        document_context (str): Relevant context from uploaded documents.
        query (str): User's input query.
        chat_history (list, optional): List of previous chats for context.

    Returns:
        str: Engineered prompt for the LLM.
    """
    # Financial questions
    if "revenue" in query.lower() or "financial" in query.lower():
        return (
            "You are a financial analyst specializing in corporate reporting and financial data interpretation. "
            "Answer the following financial question based on the document context:\n\n"
            f"Document Context:\n{document_context}\n\nQuestion: {query}\n\n"
            "If any information is missing, ask clarifying questions to complete your answer."
        )

    # Summarization requests
    elif "summarize" in query.lower():
        return (
            "You are an expert summarizer. Summarize the key facts and insights based on the following document context:\n\n"
            f"{document_context}\n\n"
            "Ensure the summary is concise, highlighting critical points only."
        )

    # Improving text and table output formatting
    elif "format" in query.lower() or "table" in query.lower():
        return (
            "You are a formatting expert. Improve the text or table formatting in the given context:\n\n"
            f"Document Context:\n{document_context}\n\n"
            "Ensure the output is well-structured, visually clear, and easy to understand."
        )

    # Follow-up questions with chat history
    elif chat_history:
        conversation = "\n".join([f"You: {h['query']}\nBot: {h['response']}" for h in chat_history])
        return (
            "You are a conversational assistant maintaining context throughout discussions. Continue this conversation while considering the context:\n\n"
            f"Conversation History:\n{conversation}\n\nNew Question: {query}"
        )

    # General queries
    else:
        return (
            "Answer the following question based on the document context:\n\n"
            f"Document Context:\n{document_context}\n\nQuestion: {query}"
        )
