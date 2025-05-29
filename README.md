# Python Code Reviewer with RAG + GitHub PR Integration

A smart Python code review assistant that uses Retrieval-Augmented Generation (RAG) with FAISS, Sentence Transformers, and OpenAI GPT-4. Supports:

✅ Real-time code reviews  
✅ `.zip` project reviews  
✅ GitHub PR review + comments  
✅ Internal guideline grounding  
✅ Download/share review results  
✅ Private repo authentication

## 🛠 Tech Stack

- OpenAI GPT-4 (Chat API)
- FAISS vector store
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Python, Gradio
- GitHub REST API (v3)

## 🚀 Features

- ✨ **RAG-Powered Context:** Leverages company-specific style guides and past reviews.
- 📁 **Zip Upload Support:** Review entire projects at once.
- 🧪 **Smart Suggestions:** Offers detailed, structured refactor recommendations.
- 🔄 **GitHub PR Integration:** Reviews PRs and posts comments automatically.
- 🔐 **Supports Private Repos:** With GitHub personal access tokens.
- 📎 **Download Reviews:** Save or share AI-generated feedback.

## 📦 Setup

1. Clone or download the project files.**

2. Create a `.env` file** in the project root (local use only) with your API keys:
- OPENAI_API_KEY=your-openai-key
- GITHUB_TOKEN=your-github-token # Optional, for GitHub PR review features

3. pip install -r requirements.txt
4. python app.py