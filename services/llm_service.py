import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_response(query, retrieved_chunks):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an expert AI software engineer.

Use the repository context below to answer the user's question.

Repository Context:
{context}

User Question:
{query}

Instructions:
- Give a clear technical explanation
- Mention important files if relevant
- Explain architecture/logic
- If answer is not found in context, say so
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        stream=True
    )

    return completion