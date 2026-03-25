import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.normpath(
            os.path.abspath(os.path.join(working_directory, file_path))
        )
        wor_dir_abs = os.path.abspath(working_directory)
        is_valid_dir = os.path.commonpath([wor_dir_abs, abs_path]) == wor_dir_abs
        if not is_valid_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        _, ext = os.path.splitext(abs_path)
        if ext != ".py":
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", abs_path]
        if args:
            for arg in args:
                command.extend(arg)
        completed = subprocess.run(
            command,
            capture_output=True,
            timeout=30,
            cwd=working_directory,
            text=True,
        )
        output = ""
        if completed.returncode != 0:
            output += f"\nProcess exited with code {completed.returncode}"
        if not completed.stdout and not completed.stderr:
            output += "\nNo output produced."
        if completed.stdout:
            output += f"\nSTDOUT: {completed.stdout}"
        if completed.stderr:
            output += f"\nSTDERR: {completed.stderr}"
        return output
    except Exception as e:
        return f"Error: executing python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs the python file at the given path, relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path relative to working directory to write the contents to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to be written at the specified file location",
            ),
        },
    ),
)
