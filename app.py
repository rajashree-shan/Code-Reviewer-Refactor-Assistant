import gradio as gr
from rag_pipeline import generate_review
from zip_utils import extract_python_files
from github_integration import review_pull_request, post_pr_comment
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# ---------- Review Utilities ----------
def save_review_to_file(text: str) -> str:
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
    tmp_file.write(text)
    tmp_file.close()
    return tmp_file.name

def review_text(code):
    if not code.strip():
        return "Paste some Python code to review.", None
    review = generate_review(code)
    file_path = save_review_to_file(review)
    return review, file_path

def review_file(file):
    if file is None:
        return "Please upload a Python (.py) file.", None
    with open(file.name, "r", encoding="utf-8") as f:
        code = f.read()
    review = generate_review(code)
    file_path = save_review_to_file(review)
    return review, file_path

def review_zip(zip_file):
    if zip_file is None:
        return "Please upload a .zip file containing Python files.", None
    py_files = extract_python_files(zip_file.name)
    if not py_files:
        return "No Python files found in the ZIP.", None
    results = []
    for filename, content in py_files.items():
        review = generate_review(content)
        results.append(f"### Review: {filename}\n{review}")
    final_result = "\n\n---\n\n".join(results)
    file_path = save_review_to_file(final_result)
    return final_result, file_path

def handle_pr(repo, pr_number, token):
    comments = review_pull_request(repo, int(pr_number), token)
    post_pr_comment(repo, int(pr_number), comments, token)
    return f"Reviewed {len(comments)} Python files. Comments posted on PR #{pr_number}."

# ---------- Gradio UI ----------
with gr.Blocks(title="Code Review Assistant") as demo:
    gr.Markdown("# AI Code Review & Refactor Assistant")
    gr.Markdown("Upload code or a `.zip` project for review. Supports GitHub PRs (even private ones).")

    with gr.Tabs():
        with gr.Tab("📝 Paste Code"):
            code_input = gr.Textbox(label="Paste Python Code", lines=20, placeholder="Paste your code here...")
            review_btn = gr.Button("Review Code")
            code_output = gr.Textbox(label="Review Suggestions", lines=20)
            download_btn = gr.File(label="Download Review")
            review_btn.click(fn=review_text, inputs=code_input, outputs=[code_output, download_btn])

        with gr.Tab("📄 Upload `.py` File"):
            file_input = gr.File(label="Upload .py file", file_types=[".py"])
            file_btn = gr.Button("Review File")
            file_output = gr.Textbox(label="Review Suggestions", lines=20)
            file_download = gr.File(label="Download Review")
            file_btn.click(fn=review_file, inputs=file_input, outputs=[file_output, file_download])

        with gr.Tab("📦 Upload Project `.zip`"):
            zip_input = gr.File(label="Upload ZIP File", file_types=[".zip"])
            zip_btn = gr.Button("Review Project")
            zip_output = gr.Textbox(label="Project Review (All .py files)", lines=30)
            zip_download = gr.File(label="Download Review")
            zip_btn.click(fn=review_zip, inputs=zip_input, outputs=[zip_output, zip_download])

        with gr.Tab("🔐 GitHub PR Reviewer"):
            repo_input = gr.Text(label="GitHub Repo (e.g., user/repo)")
            pr_input = gr.Text(label="Pull Request Number")
            token_input = gr.Text(label="GitHub Token", type="password", placeholder="Personal Access Token (for private repos)")
            pr_btn = gr.Button("Review Pull Request")
            pr_output = gr.Textbox(label="GitHub PR Review Result")
            pr_btn.click(fn=handle_pr, inputs=[repo_input, pr_input, token_input], outputs=pr_output)

if __name__ == "__main__":
    demo.launch()
