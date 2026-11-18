from pathlib import Path

base = Path(r"D:\9011_py_project\llm_projects_folder\GenAI_Exercise6 E-commerce Tool-Chatbot")

folders = [
    base / "app",
    base / "data",
]

files = [
    base / "app" / "__init__.py",
    base / "app" / "main.py",
    base / "app" / "router.py",
    base / "app" / "faq.py",
    base / "app" / "sql.py",
    base / "app" / "smalltalk.py",
    base / "data" / "faq_data.csv",
    base / ".env",
    base / "requirements.txt",
]

for folder in folders:
    folder.mkdir(parents=True, exist_ok=True)

for file in files:
    if not file.exists():
        file.touch()

print("Folder structure created at:")
print(base)