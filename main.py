from video_utils import load_mp4, download_yt_vid, convert_to_wav, time_to_seconds, trim_wav
from summarize import summarize_text as offline_summary
from summarize_API import summarize_text as online_summary
import os
import glob
import whisper
import argparse

DATA_DIR = "data"

def parse_args():
    parser = argparse.ArgumentParser(description="Video Summarizer")

    parser.add_argument(
        "input",
        type = str,
        help="Youtube link or local media file (.mp4/.mp3)"
    )

    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help="Start Time (mm:ss or ss)"
    )

    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="End time (mm:ss or ss)"
    )

    return parser.parse_args()

def main():
    args = parse_args()

    input_arg = args.input
    start_sec = time_to_seconds(args.start)
    end_sec = time_to_seconds(args.end)

    if start_sec is None:
        start_sec = 0

    if end_sec is not None and end_sec <= start_sec:
        print("Error: End time must be greater than start time.")
        return

    print("Working atm...")

    # Handle YouTube or local file input
    if input_arg.startswith('https'):
        print("Detected YouTube link.")
        download_yt_vid(input_arg)
    elif input_arg.endswith(('.mp4', '.mp3')):
        print("Detected local media file.")
        load_mp4(input_arg)
    else:
        print("Invalid input. Please provide a YouTube link or media file.")
        return

    # Find the latest media file in data/
    media_files = glob.glob(os.path.join(DATA_DIR, "*.mp4")) + glob.glob(os.path.join(DATA_DIR, "*.mp3"))
    if not media_files:
        print(f"No media files found in {DATA_DIR}!")
        return

    latest_media = max(media_files, key=os.path.getmtime)

    # Convert media to WAV
    wav_file = convert_to_wav(latest_media)
    if args.start is not None or args.end is not None:
        print(f"Trimming audio from {start_sec}s to {end_sec if end_sec else 'end'}")
        wav_file = trim_wav(wav_file, start_sec, end_sec)
    if not wav_file:
        print("Failed to convert to WAV.")
        return


    # Transcribe audio with Whisper
    print("Transcribing audio using Whisper (base model)...")
    model = whisper.load_model("base")
    result = model.transcribe(wav_file)

    print("\n--- Transcription ---\n")
    print(result["text"])

    # Save transcription to file
    base_name = os.path.splitext(os.path.basename(wav_file))[0]
    txt_path = os.path.join(DATA_DIR, f"{base_name}.txt")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"\nTranscription saved to {txt_path}")

    print("Which model would you like to use:")
    print("1. Offline (Free but not exactly good and is slower)")
    print("2. OpenAI (ChatGPT)")
    choice = input("Enter 1 or 2 to choose: ").strip()

    if choice == "1":
        # Summarize using offline LLM
        print("\nGenerating summary using offline model...")
        offline_summary(txt_path)
    
    elif choice == "2": 
        # Summarize using online/API key
        while True:
            api_key = input("Enter your OpenAI API key: ").strip()
            print("\nGenerating summary using online model...")

            try:
                online_summary(txt_path, api_key)
                print("\nSummary generated successfully.")
                break  

            except Exception as e:
                print("\nInvalid API key or request failed.")
                print("Reason:", e)

                print("\nWhat would you like to do now?")
                print("1. Switch to Offline Summary")
                print("2. Try entering API key again")
                print("3. Skip summary entirely")

                retry_choice = input("Enter 1, 2, or 3: ").strip()

                if retry_choice == "1":
                    print("\nSwitching to offline summary...")
                    offline_summary(txt_path)
                    break

                elif retry_choice == "2":
                    continue  # retry API key

                elif retry_choice == "3":
                    print("Skipping summary.")
                    break

                else:
                    print("Invalid choice, retrying API key...\n")

if __name__ == "__main__":
    main()