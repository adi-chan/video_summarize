import streamlit as st
import os
import glob
import shutil
import whisper
import warnings
import logging
from video_utils import load_mp4, download_yt_vid, convert_to_wav, time_to_seconds, trim_wav, DATA_DIR
from summarize import summarize_text as offline_summary, chunk_by_sentences_and_tokens, get_tokenizer
from summarize_API import summarize_text as online_summary

# Suppress UserWarnings (like Whisper's CPU/FP16 warnings)
warnings.filterwarnings("ignore", category=UserWarning)

# Suppress transformers pipeline warnings/logging details
logging.getLogger("transformers").setLevel(logging.ERROR)

st.title("Video Summarizer")

option = st.selectbox("Source", ["YouTube URL", "Upload File"])
video_path = None

if option == "YouTube URL":
    url = st.text_input("URL")
    if url and st.button("Process"):
        video_path = download_yt_vid(url)
else:
    uploaded_file = st.file_uploader("Upload", type=["mp4", "mp3"])
    if uploaded_file and st.button("Process"):
        os.makedirs(DATA_DIR, exist_ok=True)
        video_path = os.path.join(DATA_DIR, uploaded_file.name)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

if video_path:
    with st.spinner("Processing..."):
        wav_file = convert_to_wav(video_path)
        if wav_file:
            model = whisper.load_model("base")
            result = model.transcribe(wav_file)
            transcript_text = result["text"]
            
            tokenizer = get_tokenizer()
            chunks = chunk_by_sentences_and_tokens(transcript_text, tokenizer)
            num_chunks = len(chunks)
            
            st.subheader("Transcript")
            st.caption(f"Indexed {num_chunks} chunks from {len(transcript_text)} characters.")
            st.write(transcript_text)
            
            base_name = os.path.splitext(os.path.basename(wav_file))[0]
            txt_path = os.path.join(DATA_DIR, f"{base_name}.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(transcript_text)
                
            summary_path = offline_summary(txt_path)
            with open(summary_path, "r", encoding="utf-8") as sf:
                summary_text = sf.read()
                
            st.subheader("Summary")
            st.write(summary_text)