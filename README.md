# Video Summarizer

A simple Python project that downloads YouTube videos, extracts audio, and generates a summary using OpenAI Whisper and text summarization.


https://github.com/user-attachments/assets/fb47f94e-1cd1-41e6-8c72-4603b749b91e


# Features
- Download videos from YouTube and local files
- Convert MP4/MP3 → WAV automatically
- Transcribe and summarize video content

# Setup

## Download FFMPEG using:

## macOS
brew install ffmpeg

## Ubuntu/Debian
sudo apt install ffmpeg

## Windows
choco install ffmpeg

# Clone the git

git clone https://github.com/adi-chan/video_summarize.git

cd video_summarize

# Virtual Environment Setup

It’s recommended to use a **virtual environment** so that your project dependencies don’t interfere with system-wide packages.

## 1. Create a virtual environment

python -m venv whisper-env

## 2. Activate the environment
Windows : whisper-env\Scripts\activate 

Mac/Linux: source whisper-env/bin/activate

Arch/Fish: source whisper-env/bin/activate.fish

# Install the requirements

pip install -r requirements.txt

## With this you are done setting up the tool. If you want to use ChatGPT to find summaries, please generate an API key from https://platform.openai.com/api-keys and paste it everytime you want the tool to use ChatGPT

# Usage

## From YouTube

python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

## From a local file

python main.py "path/to/video.mp4"

## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.


