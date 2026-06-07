import os

from google.genai import types
from functions.common import is_file_in_working_dir

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        target_dir = is_file_in_working_dir(working_directory, directory)
        if not target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f"Error: \"{target_dir}\" is not a directory"
        else:
            output = [f'Success: "{directory}" is within the working directory']
            for file in os.listdir(target_dir):
                curr = os.path.join(target_dir, file)
                output.append(f"{file}: file_size={os.path.getsize(curr)} bytes, is_dir={'True' if os.path.isdir(curr) else 'False'}")
            return "\n".join(output)

    except Exception as e:
        return f"Error: {e}"

def _get_all_paths_in_dir_and_subdir(directory: str) -> list[str]:
    contents = os.listdir(directory)
    additional = []
    for content in contents:
        curr = os.path.join(directory, content)
        if os.path.isdir(curr):
            additional.extend(_get_all_paths_in_dir_and_subdir(curr))
    contents.extend(additional)
    return contents

SCHEMA_GET_FILES_INFO = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
