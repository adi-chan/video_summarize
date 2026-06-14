FROM python:3.12-slim

WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "web.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.maxUploadSize=5120"]

