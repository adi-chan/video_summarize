# The below code was the previous summarizer which ran on openai api key its better but i am not very sure if its free or not. 
# I used it for my usage was 0$ even with a lot  of testing so maybe i was on trail please look into it if you wanna use it. 
# The code runs well and summaries are better if you use this code.

import os
from openai import OpenAI

def summarize_text(file_path, api_key):
    client = OpenAI(api_key=api_key)
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    summary_file = os.path.join("data", f"{base_name}_summary.txt")

    print("Summarizing with ChatGPT...")

    prompt = f"Summarize the following text in clear, structured English:\n\n{text}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert summarizer."},
            {"role": "user", "content": prompt}
        ]
    )

    summary_text = response.choices[0].message.content.strip()
    
    summary_file = os.path.join("data", os.path.splitext(os.path.basename(file_path))[0] + "_summary_online.txt")


    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"\nOnline summary saved to {summary_file}")
    print("\n--- Summary ---\n")
    print(summary_text)
    return summary_file