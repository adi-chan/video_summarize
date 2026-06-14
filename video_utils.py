import yt_dlp # This is library which helps to download youtube videos.
import os # Helps moving files and stuff.
import subprocess 
import whisper
import os

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


def time_to_seconds(t):
    # Converts mm:ss or ss to seconds.
    
    if t is None:
        return None

    parts = t.split(":")
    if len(parts) == 1:
        return int(parts[0])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    else:
        raise ValueError("Invalid time format. Use mm:ss or ss")


def trim_wav(input_wav, start_sec, end_sec):

    output_wav = input_wav.replace(".wav", "_trimmed.wav")

    cmd = ["ffmpeg", "-y", "-loglevel", "warning", "-ss", str(start_sec), "-i", input_wav]

    if end_sec is not None:
        cmd += ["-to", str(end_sec)]

    cmd += ["-c", "copy", output_wav]

    subprocess.run(cmd, check=True)
    return output_wav


COOKIES_PATH = os.path.expanduser("~/cookies.txt")

def download_yt_vid(url):
    ydl_opts = {
        'outtmpl': os.path.join(DATA_DIR, '%(title)s.%(ext)s'),  # Save in data/ folder
        'format': 'bestaudio/best',                              # Pick best video/audio.
        'postprocessors': [{                                     # Convert to mp3 after download
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],                          
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True
    }

    if os.path.exists(COOKIES_PATH):
        ydl_opts['cookiefile'] = COOKIES_PATH

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        base, _ = os.path.splitext(filename)
        return base + ".mp3"

def load_mp4(file_path):
    if os.path.exists(file_path) and (file_path.endswith(".mp4") or file_path.endswith(".mp3")):   
        print(f"Your file has been found at {file_path}")           
        dest = os.path.join(DATA_DIR, os.path.basename(file_path))    
        import shutil
        shutil.copy(file_path, dest)
        print(f"Copied to {dest}")
        return dest
    else:
        print("File not found or not an valid path!")
        return None

def convert_to_wav(video_path):
    if not os.path.exists(video_path): 
        print("Video not found.")
        return None

    Original = os.path.splitext(os.path.basename(video_path))[0] 
    wav_path = os.path.join("data", f"{Original}.wav")

    command = [
        "ffmpeg",
        "-y",
        "-loglevel", "warning",
        "-i", video_path,    # input video
        "-vn",               # no video
        "-acodec", "pcm_s16le", # WAV format
        "-ar", "16000",      # sample rate (Whisper native so its in sync)
        "-ac", "1",          # mono (Whisper native)
        wav_path
    ]

    print(f"Converting {video_path} → {wav_path} ...")
    subprocess.run(command, check=True)
    print("Conversion done!")

    return wav_path
    
    