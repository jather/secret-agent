import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_directory = os.path.join(working_directory, directory)
    target_cleaned = os.path.normpath(os.path.abspath(target_directory))
    is_valid_path = (
        os.path.commonpath([working_dir_abs, target_cleaned]) == working_dir_abs
    )
    if not is_valid_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'

    directory_name = repr(directory) if directory != "." else "current"
    file_info = f"Result for {directory_name} directory:"

    files_list = os.listdir(target_directory)
    for file_name in files_list:
        path = os.path.join(target_directory, file_name)
        try:
            file_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
        except Exception as e:
            file_info = f"Error: {e}"
            return file_info

        file_info += f"\n- {file_name}: file_size={file_size}, is_dir={is_dir}"
    return file_info


schema_get_files_info = types.FunctionDeclaration(
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
