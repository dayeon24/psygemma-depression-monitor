import torch
from transformers import pipeline
import os
import json

model_id = "google/medgemma-1.5-4b-it"

pipe = pipeline(
    "text-generation",
    model=model_id,
    trust_remote_code=True,
    device_map="auto",
    do_sample=False,
    temperature=0.0
)

# 1. JSON 데이터 로드
file_path = "../examples/sample_diaries.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

patient_id = data["user_id"]
posts = data["posts"]

all_analyzed_diaries = []

for post in posts:
    date_str = post["t"] 
    body_content = post["body"]

    query = f"""
    A patient’s recent diary entry is provided below.

    {body_content}

    Based on the content, assess whether this raises concern for depressive disorder.
    Briefly state your clinical impression, cite relevant sentences from the diary that support your reasoning, and summarize in 1–2 sentences.
    Maintain a professional clinical tone. This is not a formal diagnosis.
    """

    instruction = "Provide a concise structured output."
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query + instruction}
            ]
        }
    ]


    # Execution and Output
    output = pipe(messages, max_new_tokens=2000) 
    raw_response = output[0]["generated_text"][-1]["content"]
    all_analyzed_diaries.append({
        "date": date_str,
        "content":body_content,
        "raw":raw_response
    })
    print(raw_response)

with open(f"../examples/PsyGemma_output.json","w") as fw:
    json.dump(all_analyzed_diaries, f, ensure_ascii=False, indent=2)
