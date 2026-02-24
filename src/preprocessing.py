import json
import re
from datetime import datetime

def process_patient_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed_list = []

    for item in data:
        content = item['content']
        raw = item['raw']
        
        # 1. Evidence Sentences 추출
        evidence_sentences = re.findall(r'"([^"]*)"', raw)
        
        # 2. 원본 Content에 하이라이트 적용 (클래스: evidence-mark로 단순화)
        highlighted_content = content
        for sentence in set(evidence_sentences):
            clean_sentence = sentence.strip()
            if len(clean_sentence) > 5 and clean_sentence in highlighted_content:
                highlighted_content = highlighted_content.replace(
                    clean_sentence, 
                    f'<mark class="evidence-mark">{clean_sentence}</mark>'
                )

        # 3. Summary 섹션 추출 및 노이즈 제거
        summary_match = re.search(r'\*\*Summary:\*\*\s*(.*?)(?=\n\n|\n\*\*|$)', raw, re.DOTALL)
        ai_summary = summary_match.group(1).strip() if summary_match else "No specific summary provided."
        # 줄바꿈 제거 (한 줄 요약 스타일 유지)
        ai_summary = ai_summary.replace('\n', ' ')

        # 4. Clinical Impression 섹션 추출 (Status 판별용)
        impression_match = re.search(r'\*\*Clinical Impression:\*\*\s*(.*?)(?=\n\n\*\*|\n\*|$)', raw, re.DOTALL)
        clinical_impression = impression_match.group(1).strip() if impression_match else ""

        # 5. 상태(Status) 및 색상 결정 로직
        full_text_lower = (ai_summary + " " + clinical_impression).lower()
        
        critical_indicators = [
            'suicidal ideation', 'suicidal thoughts', 'self-harm', 'self-destructive',
            'immediate clinical intervention', 'urgent clinical attention', 'high level of concern'
        ]
        observation_indicators = [
            'significant distress', 'functional impairment', 'worsening symptoms',
            'requires further evaluation', 'warrants further assessment', 'concern for depressive'
        ]

        if any(word in full_text_lower for word in critical_indicators):
            status = "CRITICAL"
            color = "red"
        elif any(word in full_text_lower for word in observation_indicators):
            status = "OBSERVATION"
            color = "yellow"
        else:
            status = "NORMAL"
            color = "green"

        # 6. 결과 리스트에 담기 (원하시는 형식 반영)
        processed_list.append({
            "date": datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
            "status": status,
            "color": color,
            "ai_summary": ai_summary,
            "original_content": highlighted_content,
            "annotations": []  # 추후 수동 메모 등을 위한 빈 리스트
        })

    # 날짜 최신순 정렬
    processed_list.sort(key=lambda x: x['date'], reverse=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_list, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    process_patient_data('./examples/PsyGemma_output.json', './examples/processed_data.json')