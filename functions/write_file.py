import os


def write_file(working_directory, file_path, content):
    abs_path = os.path.normpath(
        os.path.abspath(os.path.join(working_directory, file_path))
    )
    abs_wor_dir = os.path.abspath(working_directory)
    is_valid_path = os.path.commonpath([abs_path, abs_wor_dir]) == abs_wor_dir
    if not is_valid_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(abs_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    try:
        with open(abs_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
