# 02 — E-commerce Assistant

Multi-route chatbot that handles:

- Small-talk
- FAQ (RAG with Chroma)
- Product questions (text-to-SQL on SQLite)

Built with OpenAI, semantic-router, ChromaDB, and Streamlit.

## Run

```bash
# Activate the shared venv, then:
streamlit run app/main.py
```
Requires .env with OPENAI_API_KEY and OPENAI_MODEL.

```text

### 3. Git steps (run these in PowerShell)

```powershell
# 1. Clone the repo (if you don’t already have it)
cd D:\9011_py_project\llm_projects_folder
git clone https://github.com/yash9614/project_streak_.git
cd project_streak_

# 2. Create the new project folder
mkdir projects\02-ecommerce-assistant

# 3. Copy your finished project into it
# (adjust source path if needed)
Copy-Item -Path "D:\9011_py_project\llm_projects_folder\GenAI_Exercise6 E-commerce Tool-Chatbot\*" -Destination "projects\02-ecommerce-assistant" -Recurse -Force

# 4. Add the two files we just created (requirements.txt + README.md)
# Make sure they are inside projects\02-ecommerce-assistant\

# 5. Update the main README (optional but recommended)
# Open README.md and add a new row in the projects table for 02.

# 6. Stage, commit, push
git add projects/02-ecommerce-assistant
git status   # verify only the new folder is staged
git commit -m "Add 02-ecommerce-assistant (semantic router + FAQ RAG + text-to-SQL)"
git push origin main
```
mportant
Do not copy the .venv or any __pycache__ folders.
Keep your .env out of the commit (it should already be in .gitignore).