import os
import subprocess


def read_file(path):
    """Read and return the contents of a text file.
    Args:
        path: Path to the file to read.
    """
    with open(path,"r") as infile:
        return infile.read()

def list_files(path):
    """Return a list of all files in a given directory.
    Args:
        path: Path to the directory to list files from.
    """
    ignored = [".venv", "__pycache__", ".git"]
    files = os.listdir(path)
    filtered = []
    for file in files:
        if file not in ignored:
            filtered.append(file)

    return filtered

def write_file(path, content):
    """Create or overwrite a file with the provided content.
    Args:
        path: Path to the file to write.
        content: Content to write into the file.
    """
    with open(path, "w") as outfile:
        outfile.write(content)
    return f"Successfully wrote to {path}"

def edit_file(path, old_text , new_text):
    """Edit existing code in a file
    Args:
        path: Path to the file to edit.
        old_text: Old content to edit on the file.
        new_text: New content to write.
    """
    with open(path, "r") as infile:
        content = infile.read()
        if old_text in content:
            content = content.replace(old_text, new_text)
            with open(path, "w") as outfile:
                outfile.write(content) 
            return f"Successfully edited to {path}"
        else:
            return "Error: old text was not found in the file."

def run_python(path):
    """Run a Python file and return its output and errors.

    Args:
        path: Path to the Python file to execute.
    """
    result = subprocess.run(
        ["python3", path],
        capture_output=True,
        text=True,
        timeout=10
    )

    return result.stdout + result.stderr

