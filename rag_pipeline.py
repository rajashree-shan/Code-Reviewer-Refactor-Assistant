import os
from embedding_store import retrieve_relevant_chunks
from openai import OpenAI

# Create the OpenAI client using the new syntax
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_review(code: str) -> str:
    context = retrieve_relevant_chunks(code)

    prompt = f"""
You are a senior software engineer performing a code review. Evaluate the following Python code using these 8 criteria:

1. **Readability & Style**
2. **Code Quality & Best Practices**
3. **Performance & Efficiency**
4. **Testability**
5. **Security**
6. **Architecture & Design**
7. **Documentation & Comments**
8. **Error Handling**

Return the review as a **structured markdown report**, with a heading for each of these sections. Be constructive, give examples, and suggest improvements.

---

Code:
{code}

Relevant Guidelines and Past Reviews:
{context}

Return structured review and refactor suggestions.
"""

    # Call GPT-4 using the new API client
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
