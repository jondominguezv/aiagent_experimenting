import os

from google.genai import types
from functions.common import is_file_in_working_dir

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        target_file = is_file_in_working_dir(working_directory, file_path)
        if not target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as file:
            file.write(content)
    except Exception as e:
        return f'Error: {e}'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

SCHEMA_WRITE_FILE = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a specified file relative to the working directory with provided content string, provides status of file write.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written the given file",
            ),
        },
        required=["file_path", "content"]
    ),
)
