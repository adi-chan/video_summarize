from transformers import pipeline
import os
import re
from tqdm import tqdm

summarizer = None
tokenizer = None

def get_summarizer():
    global summarizer
    if summarizer is None:
        from transformers import pipeline
        print("Loading offline summarization model (facebook/bart-large-cnn)...")
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
    return summarizer

def get_tokenizer():
    global tokenizer
    if tokenizer is None:
        from transformers import AutoTokenizer
        print("Loading tokenizer (facebook/bart-large-cnn)...")
        tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    return tokenizer

def chunk_by_sentences_and_tokens(text, tokenizer, max_tokens=900, overlap_sentences=2):
    # Split text into sentences cleanly using Regex
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Get the token count for each individual sentence
    sentence_lengths = [len(tokenizer.encode(s, add_special_tokens=False)) for s in sentences]
    
    chunks = []
    start = 0
    
    # Slide the window through the sentences
    while start < len(sentences):
        end = start
        current_tokens = 0
        
        # Add sentences until we hit the token limit
        while end < len(sentences) and current_tokens + sentence_lengths[end] <= max_tokens:
            current_tokens += sentence_lengths[end]
            end += 1
            
        # Edge case: A single sentence is longer than max_tokens
        if end == start:
            chunks.append(sentences[start])
            start += 1  # Move past it to avoid infinite loop
        else:
            # Combine the sentences for this chunk
            chunks.append(" ".join(sentences[start:end]))
            
            if end == len(sentences):
                break  # Reached the end of the text
                
            # Slide start index forward, leaving an overlap of sentences
            # max(start + 1, ...) guarantees the loop always makes progress
            start = max(start + 1, end - overlap_sentences)
            
    return chunks

def summarize_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    tokenizer = get_tokenizer()
    sum_pipeline = get_summarizer()

    # Initial chunking
    chunks = chunk_by_sentences_and_tokens(text, tokenizer, max_tokens=900, overlap_sentences=2)

    if len(chunks) == 1:
        # Single chunk: summarize once (keeps all key details of a short video)
        print("\nGenerating summary...")
        final_summary = sum_pipeline(
            chunks[0],
            max_length=250,
            min_length=80,
            do_sample=False
        )[0]['summary_text']
    else:
        # Multiple chunks: summarize each chunk individually
        print(f"\nProcessing {len(chunks)} chunks...")
        summaries = []
        for c in tqdm(chunks, desc="Summarizing chunks", ascii=True):
            summary = sum_pipeline(
                c, 
                max_length=250, 
                min_length=80, 
                do_sample=False
            )[0]['summary_text']
            summaries.append(summary)
            
        final_summary = " ".join(summaries)
        
        # Recursive compression only triggers if the combined summaries are extremely long (> 600 words)
        if len(final_summary.split()) > 600:
            print("\nCombined summary is very long. Condensing recursively...")
            chunks = chunk_by_sentences_and_tokens(final_summary, tokenizer, max_tokens=900, overlap_sentences=1)
            while len(chunks) > 1:
                summaries = []
                for c in tqdm(chunks, desc="Condensing", ascii=True):
                    summary = sum_pipeline(c, max_length=200, min_length=60, do_sample=False)[0]['summary_text']
                    summaries.append(summary)
                combined = " ".join(summaries)
                chunks = chunk_by_sentences_and_tokens(combined, tokenizer, max_tokens=900, overlap_sentences=1)
            
            final_summary = sum_pipeline(
                chunks[0],
                max_length=300,
                min_length=100,
                do_sample=False
            )[0]['summary_text']

    summary_file = os.path.join("data", os.path.splitext(os.path.basename(file_path))[0] + "_summary_offline.txt")
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(final_summary)

    print(f"\nOffline summary saved to {summary_file}\n")
    print(final_summary)
    return summary_file