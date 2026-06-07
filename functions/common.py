import os

def is_file_in_working_dir(working_directory: str, file_path: str) -> bool | str:
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
    is_in_path = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs
    if not is_in_path:
        return False
    return target_file