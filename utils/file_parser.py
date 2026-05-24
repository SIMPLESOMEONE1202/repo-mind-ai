import os

# Folders to ignore
IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    "dist",
    "build",
    ".next",
    ".idea",
    ".vscode"
}

# File extensions to process
ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".cs",
    ".go",
    ".rb",
    ".php",
    ".html",
    ".css",
    ".json",
    ".md",
    ".txt",
    ".yaml",
    ".yml"
}


def get_repository_files(repo_path):

    repository_files = []

    for root, dirs, files in os.walk(repo_path):

        # Ignore unwanted directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:

            file_extension = os.path.splitext(file)[1]

            if file_extension in ALLOWED_EXTENSIONS:

                full_path = os.path.join(root, file)

                repository_files.append(full_path)

    return repository_files


def read_file_content(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except Exception:
        return None