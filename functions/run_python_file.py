import subprocess
import os

from google.genai import types
from functions.common import is_file_in_working_dir

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        target_file = is_file_in_working_dir(working_directory, file_path)
        if not target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)

        python_run = subprocess.run(
            command,
            cwd=working_directory,
            text=True,
            timeout=30,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        returncode, stdout, stderr = python_run.returncode, python_run.stdout, python_run.stderr

        if returncode != 0:
            return f"Process exited with code {returncode}"
        elif not stdout and not stderr:
            return "No output produced"
        else:
            return f"STDOUT:{stdout}\nSTDERR:{stderr}"
        
    except Exception as e:
        return f"Error: executing Python file: {e}"

SCHEMA_RUN_PYTHON_FILE = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified Python file relative to the working directory, accepts optional command line args, provides the STDOUT and STDERR if return code was 0.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of command line arguments",
                items=types.Schema(
                    type=types.Type.STRING
                )
            ),
        },
        required=["file_path", "args"]
    ),
)
