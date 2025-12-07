from transformers import pipeline
import os

# device=-1 uses CPU by default
# if you want to use GPU, change device=-1 to device=0
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def summarize_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split into chunks for long texts
    max_chunk_size = 1000
    chunks = []
    while len(text) > max_chunk_size:
        split_at = text.rfind(" ", 0, max_chunk_size)
        chunks.append(text[:split_at])
        text = text[split_at:]
    chunks.append(text)

    # Summarize chunks
    summaries = [summarizer(c, max_length=150, min_length=40, do_sample=False)[0]['summary_text'] for c in chunks]
    final_summary = " ".join(summaries)

    summary_file = os.path.join("data", os.path.splitext(os.path.basename(file_path))[0] + "_summary_offline.txt")
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(final_summary)

    print(f"\nOffline summary saved to {summary_file}\n")
    print(final_summary)
    return summary_file