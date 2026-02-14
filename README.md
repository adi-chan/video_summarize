# Video Summarizer

A Dockerized Python-based video transcription and summarization tool that downloads videos (YouTube/local), extracts audio, and generates summaries using OpenAI Whisper and Transformer-based models.

Supports offline models and optional OpenAI API integration.

---

## Demo

### Docker
https://github.com/user-attachments/assets/68517926-ee34-4a89-8d48-b829e11ff7ba

### Python
https://github.com/user-attachments/assets/b190be11-d842-4eac-8f1e-8fc5cdd70999

---

## Features

- Download videos from YouTube or process local media files
- Automatic MP4/MP3 → WAV conversion
- Timestamp-based trimming (--start, --end)
- Transcription using Whisper
- Offline summarization using Transformers
- Optional OpenAI API support
- CLI-based interface
- ~3.5× real-time processing speed on CPU
- Containerized via Docker

---

## Setup (Docker Recommended)

### Install Docker

#### Arch Linux:

1. sudo pacman -S docker  
2. sudo systemctl start docker  
3. sudo systemctl enable docker  
4. sudo usermod -aG docker $USER  

5. Log out and log back in, then verify:

6. docker run hello-world

#### macOS / Windows:

1. Download Docker Desktop from:  
https://www.docker.com/products/docker-desktop/

2. Verify installation:

docker run hello-world

---

### Clone Repository

git clone https://github.com/adi-chan/video_summarize.git  
cd video_summarize  

---

### Build Docker Image

docker build -t video_summarize .

---

### Run

#### From YouTube:

docker run -it \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -v $(pwd)/data:/app/data \
  video_summarize \
  python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

#### From local file:

docker run -it \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -v $(pwd)/data:/app/data \
  video_summarize \
  python main.py "path/to/video.mp4"

Models download once and are cached locally.

---

## Manual Setup (Without Docker)

Recommended Python version: 3.10–3.12

### Create virtual environment:

python -m venv whisper-env  
source whisper-env/bin/activate  

### Install dependencies:

#### CPU only:

pip install torch --index-url https://download.pytorch.org/whl/cpu  

#### NVIDIA GPU:

pip install torch  

Then:

pip install yt-dlp ffmpeg-python openai-whisper transformers numpy gpt4all  

#### Install ffmpeg:

macOS:
brew install ffmpeg  

Ubuntu/Debian:
sudo apt install ffmpeg  

Windows:
choco install ffmpeg  

---

## OpenAI API (Optional)

1. Get API key from https://platform.openai.com/api-keys  
2. Never share your API key  
3. Provide it when prompted  

---

## Performance

- Processes videos at ~3.5× real-time speed on CPU  
- Achieves ~80–85% semantic alignment with reference summaries  
- Reproducible via Docker with pinned dependency versions  

---

# License

This project is licensed under the [MIT License](LICENSE).

