import google.generativeai as genai
import os
from app.config import GOOGLE_API_KEY,MODEL_NAME

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)


def generate_response(query, docs):
    context = "\n\n".join([
        f"{doc['section']}:\n{doc['content']}"
        for doc in docs
    ])

    prompt = f"""
You are a healthcare insurance policy assistant.

STRICT RULES:
- Answer ONLY using the provided context
- Do NOT make up information
- Do NOT ask for more context
- If answer is not found, say: "Not found in UHC policy documents"

STRUCTURE YOUR ANSWER:
1. Coverage: When the procedure is covered
2. Not Covered: When it is not covered
3. Criteria: Key clinical or policy requirements

Be precise, clinical, and structured.

Context:
{context}

Question:
{query}

Answer:
"""

    response = model.generate_content(prompt)

    return response.text