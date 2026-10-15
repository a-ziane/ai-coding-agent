import os
import subprocess
import shlex
from pathlib import Path


def read_file(path):
    """Read and return the contents of a text file.
    Args:
        path: Path to the file to read.
    """
    try:
        path = resolve_project_path(path)
        with open(path,"r") as infile:
            return infile.read()
    except (ValueError, OSError) as error:
        return f"Error: {error}"
    
    
#####################################################################
def list_files(path):
    """Return a list of all files in a given directory.
    Args:
        path: Path to the directory to list files from.
    """
    try:
        path = resolve_project_path(path)
        ignored = [".venv", "__pycache__", ".git"]
        files = os.listdir(path)
        filtered = []
        for file in files:
            if file not in ignored:
                filtered.append(file)   
        return filtered
    except (ValueError, OSError) as error:
        return f"Error: {error}"
#####################################################################
def write_file(path, content):
    """Create or overwrite a file with the provided content.
    Args:
        path: Path to the file to write.
        content: Content to write into the file.
    """
    try:
        path = resolve_project_path(path)
        with open(path, "w") as outfile:
            outfile.write(content)
        return f"Successfully wrote to {path}"
    except (ValueError, OSError) as error:
        return f"Error: {error}"
#####################################################################
def edit_file(path, old_text , new_text):
    """Edit existing code in a file
    Args:
        path: Path to the file to edit.
        old_text: Old content to edit on the file.
        new_text: New content to write.
    """
    try:
        path = resolve_project_path(path)
        if not old_text:
            return f"Error: old_text must not be empty"
        with open(path, "r") as infile:
            content = infile.read()
            if old_text in content:
                content = content.replace(old_text, new_text)
                with open(path, "w") as outfile:
                    outfile.write(content) 
                return f"Successfully edited to {path}"
            else:
                return "Error: old text was not found in the file."
    except (ValueError, OSError) as error:
        return f"Error: {error}"


#####################################################################
PROJECT_ROOT = Path(__file__).resolve().parent

ALLOWED_COMMANDS = {
    "python3",
    "pytest",
    "node",
    "npm"
}

def run_command(command: str) -> str:
    """
    Run an approved development command inside the project directory
    Use this tool for JavaScript files, Python tests, npm scripts.

    Allowed command names:
    -python3
    -pytest
    -node
    -npm

    Examples:
    -node test.js
    -pytest
    -pytest tests/test_tools.py
    -npm test
    python3 example.py

    Args: 
        command: the complete command to run.
    Returns:
        the command, working directory, exit code, stdout, and stderr

    """
    try:
        arguments = shlex.split(command)
    except ValueError as error:
        return f"Error: Invalid command syntax: {error}"

    if not arguments:
        return "Error: No command was provided"
    
    executable = arguments[0]

    if executable not in ALLOWED_COMMANDS:
        allowed = ", ".join(sorted(ALLOWED_COMMANDS))
        return(
            f"Error: Command '{executable}' is not allowed. \n"
            f"Allowed commands: {allowed}"
        )
    
    
    try:
        result = subprocess.run(
            arguments,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            shell=False
        )

        stdout = result.stdout.strip() or "(empty)"
        stderr = result.stderr.strip() or "(empty)"

        return(
            f"Command: {command}\n"
            f"Working directory: {PROJECT_ROOT}\n"
            f"Exit code: {result.returncode}\n"
            f"STDOUT:\n{stdout}\n"
            f"STDERR:\n{stderr}\n"
        )
    except subprocess.TimeoutExpired:
        return(
            f"Command: {command}\n"
            "Error: Command timed out after 30 seconds."
        )
    except FileNotFoundError:
        return(
            f"Error: '{executable}' is allowed but is not installed"
            "or could not be found."
        )
    except Exception as error:
        return f"Error while running command: {error}"

#############################################################################
def resolve_project_path(path):
    """Resolves the path into an absolute path
    Args:
        path: the path of the intended file
    """
    path_obj = Path(path)
    if not path_obj.is_absolute():
        path_obj = PROJECT_ROOT/path_obj
    path_resolved = path_obj.resolve()
    if path_resolved.is_relative_to(PROJECT_ROOT):
        return path_resolved
    else:
        raise ValueError("Access denied: path is outside the project.")
