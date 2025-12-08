# Video Summarizer

A simple Python project that downloads YouTube videos, extracts audio, and generates a summary using OpenAI Whisper/Offline models.

# Demo 

https://github.com/user-attachments/assets/b190be11-d842-4eac-8f1e-8fc5cdd70999

## Features
- Download videos from YouTube
- Convert MP4/MP3 → WAV automatically
- Transcribe and summarize video content

## Setup

git clone https://github.com/adi-chan/video_summarize.git

cd video_summarize

It’s recommended to use a **virtual environment** so that your project dependencies don’t interfere with system-wide packages.

## 1. Create a virtual environment

python -m venv whisper-env

## 2. Activate the environment
Windows : whisper-env\Scripts\activate 

Mac/Linux: source whisper-env/bin/activate

Arch/Fish: source whisper-env/bin/activate.fish

## 3. Install the requirement 

pip install -r requirements.txt

## If faced with any errors, install them using these commands.

pip install torch --index-url https://download.pytorch.org/whl/cpu

pip install yt-dlp ffmpeg-python openai-whisper transformers numpy gpt4all

## Then download FFMPEG in another terminal outside of the env so it downloads its all over the desktop using:

## macOS
brew install ffmpeg

## Ubuntu/Debian
sudo apt install ffmpeg

## Windows
choco install ffmpeg


# The tool works with chatgpt too for that you will need an api key, if you want to use offline models skip this part.

1. https://platform.openai.com/api-keys
   
2. Make an api key but never share it with anyone.
   
3. Set it up while being in the whisper env.
   
## macOS/Linux

export OPENAI_API_KEY="your_api_key_here"

## Arch

set -x set -x OPENAI_API_KEY "your_api_key_here"

## Windows (PowerShell)

setx OPENAI_API_KEY "your_api_key_here"


# Usage: While being in the whisper env run these commands

# From YouTube

python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# From a local file

python main.py "path/to/video.mp4" 

# License

This project is licensed under the [MIT License](LICENSE).

