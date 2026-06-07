import os


from config import FILE_CONTENT_LIMIT
from google.genai import types
from functions.common import is_file_in_working_dir

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target_file = is_file_in_working_dir(working_directory, file_path)
        if not target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file) as file:
            contents = file.read(FILE_CONTENT_LIMIT)
            if file.read(1):
                contents += f'[...File "{file_path}" truncated at {FILE_CONTENT_LIMIT} characters]'
    except Exception as e:
        return f'Error: {e}'
    return contents

SCHEMA_GET_FILE_CONTENT = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Gets file content in a specified file relative to the working directory, providing file contents up to {FILE_CONTENT_LIMIT} characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)
