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
    diary_content = f.read()

    # Following your exact query format
    query = f"""
    Analyze the following personal diary entries to assist in a clinical psychiatric evaluation:

    [Diary Content]
    {diary_content}

    Requirements:
    1. Identify clinical observations and 🚨 Red Flags (e.g., suicidal ideation, psychomotor retardation) relevant to a mental health professional.
    2. Provide diagnostic criteria-based insights (e.g., DSM-5) to determine if this individual meets the threshold for a clinical patient.
    """

    # Following your exact instruction format
    instraction = "Please provide a concise, professional medical output."

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query + instraction}
            ]
        }
    ]


    # Execution and Output
    output = pipe(messages, max_new_tokens=2000) 
    raw_response = output[0]["generated_text"][-1]["content"]

with open(f"../examples/report.json","w") as fw:
    json.dump(raw_response, fw, ensure_ascii=False, indent=2)
