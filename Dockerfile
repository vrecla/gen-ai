# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /pdf-chat-app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Clear pip cache to avoid conflicts
RUN pip cache purge

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Upgrade dependecies
RUN python -m pip install --upgrade streamlit-extras
RUN python -m pip install --upgrade streamlit

# RUN python -m pip install --upgrade langchain langchain-community
RUN pip install openai==0.28.1 langchain==0.0.316

# Set PYTHONPATH to include /pdf-chat-app
ENV PYTHONPATH=/pdf-chat-app

ENV HTTP_PROXY=""
ENV HTTPS_PROXY=""

# Expose Streamlit default port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]