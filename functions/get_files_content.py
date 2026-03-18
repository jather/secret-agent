import os
import config


def get_files_content(working_directory, file_path):
    full_path = os.path.normpath(
        os.path.abspath(os.path.join(working_directory, file_path))
    )
    wor_dir_abs = os.path.abspath(working_directory)
    is_valid_path = os.path.commonpath([wor_dir_abs, full_path]) == wor_dir_abs
    print(full_path)
    if not is_valid_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    file_content_string = ""
    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(config.MAX_CHARS)
            if f.read(1):
                file_content_string += (
                    f"[...File {file_path} truncated at 10000 characters]"
                )
    except Exception as e:
        return f"Error: {e}"
    return file_content_string
