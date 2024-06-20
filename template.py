from pathlib import Path

#######################################################################################
#####                                                                             #####
#####                             Project needed files                            #####
#####                                                                             #####
#######################################################################################

list_of_files = [
    ".github/workflows/main.yaml",
    "src/__init__.py",
    "src/get_embedding_function.py",
    "src/query_data.py",
    "src/populate_database.py",
    "static/style/style.py",
    "tests/__init__.py",
    "tests/test_app.py",
    "requirements.txt",
    "Makefile",
    "App.py",
    "notebooks/experiments.ipynb"
]

#######################################################################################
#####                                                                             #####
#####                            Project Requirements                             #####
#####                                                                             #####
#######################################################################################

requirements_list = [ 
    "pytest",
    "pytest-cov",
    "pylint",
    "fire",
    "black",
    "streamlit",
    "ipython",
    "pypdf",
    "langchain",
    "chromadb # Vector storage",
    "groq",
    "langchain-core",
    "langchain-groq",
    "gradio",
    "llama-index",
    "langchain_community",
    "dvc",
    "dvc-gdrive"
]

#######################################################################################
#####                                                                             #####
#####                              Makefile commands                              #####
#####                                                                             #####
#######################################################################################

makefile_list = [
    "install:\n\tpip install --upgrade pip &&\\\n\t\tpip install -r requirements.txt",
    "test:\n\tpython -m pytest -vv --cov=src tests/test_*.py",
    "format:\n\tblack *.py src/*.py tests/test_*.py",
    "lint:\n\tpylint --disable=R,C *.py src/*.py tests/test_*.py",
    "run:\n\tstreamlit run App.py",
    "all: install lint test",
    "ollama:\n\tcurl -fsSL https://ollama.com/install.sh | sh",
    "nomic-embed-text:\n\tollama pull nomic-embed-text",
    "llama3:\n\tollama pull llama3"
]

#######################################################################################
#####                                                                             #####
#####                           Creating Needed files                             #####
#####                                                                             #####
#######################################################################################

for filepath in list_of_files:
    filepath = Path(filepath)
    if not filepath.parent.exists():
        filepath.parent.mkdir(parents=True, exist_ok=True)

    if (not filepath.exists()) or (filepath.stat().st_size == 0):
        if filepath.name == "requirements.txt":
            with filepath.open("w", encoding="utf-8") as f:
                for requirement in requirements_list:
                    f.write(requirement + "\n")
        elif filepath.name == "Makefile":
            with filepath.open("w", encoding="utf-8") as f:
                for makeline in makefile_list:
                    f.write(makeline + "\n")
        else:
            filepath.touch()  # create an empty file


#######################################################################################
#####                                                                             #####
#####                            Add Items to .gitignore                          #####
#####                                                                             #####
#######################################################################################

gitignore_path = Path(".gitignore")
gitignore_entries = ["/data/", "/chroma/"]

# Read existing .gitignore content
if gitignore_path.exists():
    with gitignore_path.open("r", encoding="utf-8") as f:
        existing_lines = f.read().splitlines()
else:
    existing_lines = []

# Append new entries if they don't already exist
with gitignore_path.open("a", encoding="utf-8") as f:
    for entry in gitignore_entries:
        if entry not in existing_lines:
            f.write(entry + "\n")
