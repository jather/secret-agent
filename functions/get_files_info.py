import os


def get_files_info(working_directory, directory="."):
    target_directory = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(target_directory)
    if not abs_path.startswith(os.path.abspath(working_directory)):
        raise ValueError(
            f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        )
    if not os.path.isdir(target_directory):
        raise ValueError(f'Error: "{directory}" is not a directory')

    directory_name = repr(directory) if directory != "." else "current"
    print(f"Result for {directory_name} directory:")
    files_list = os.listdir(target_directory)
    for file_name in files_list:
        path = os.path.join(target_directory, file_name)
        try:
            file_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
        except Exception as e:
            print("Error:", e)

        print(f"- {file_name}: file_size={file_size}, is_dir={is_dir}")
