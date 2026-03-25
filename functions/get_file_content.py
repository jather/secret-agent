import os
import config
from google.genai import types


def get_file_content(working_directory, file_path):
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


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="get the contents of the file at the given path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path relative to the working directory with the file whose contents we want to get.",
            ),
        },
    ),
)
