import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
            working_dir_abs = os.path.abspath(working_directory)
            target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
            valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        
            if valid_target_file is not True:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
            elif os.path.isfile(target_file) == False:
                return f'Error: "{file_path}" does not exist or is not a regular file'

            elif target_file.endswith('.py') == False:
                return f'Error: "{file_path}" is not a Python file'

            command = ["python", target_file]
            if args:
                 command.extend(args)
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
            if result.returncode != 0:
                return f'Process exited with with code {result.returncode}'
            elif result.stdout == "" and result.stderr == "":
                return f'No output produced'
            return f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'
    except Exception as e:
         return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file in the specified working directory with optional arguments, returning the standard output and standard error of the execution",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional arguments to pass to the Python file",
                }
            },
            "required": ["file_path"]
        }
    },
}