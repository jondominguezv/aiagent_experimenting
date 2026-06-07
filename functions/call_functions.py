from collections.abc import Callable
from google.genai import types

from functions.get_files_info import SCHEMA_GET_FILES_INFO, get_files_info
from functions.get_file_content import SCHEMA_GET_FILE_CONTENT, get_file_content
from functions.run_python_file import SCHEMA_RUN_PYTHON_FILE, run_python_file
from functions.write_file import SCHEMA_WRITE_FILE, write_file

AVAILABLE_FUNCTIONS = [
    types.Tool(function_declarations=[
        SCHEMA_GET_FILES_INFO,
        SCHEMA_GET_FILE_CONTENT,
        SCHEMA_RUN_PYTHON_FILE,
        SCHEMA_WRITE_FILE,
    ])
]

FUNCTION_MAP = {
    SCHEMA_GET_FILES_INFO.name: get_files_info,
    SCHEMA_GET_FILE_CONTENT.name: get_file_content,
    SCHEMA_RUN_PYTHON_FILE.name: run_python_file,
    SCHEMA_WRITE_FILE.name: write_file,
}

WORKING_DIR = "./calculator"

def call_function(
    function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:
    func_log = f"Calling function: {function_call.name}"
    func_log = func_log + f"({function_call.args})" if verbose else func_log
    print(func_log)

    func_name = function_call.name or ""

    if func_name not in FUNCTION_MAP:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = WORKING_DIR

    func_result = FUNCTION_MAP[func_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": func_result},
            )
        ],
    )