import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    
        if valid_target_file is not True:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        elif os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" is not a file'

        with open(target_file, 'r') as f:
            content = f.read()
            if len(content) > MAX_CHARS:
                content += f"...File {file_path} truncated to {MAX_CHARS} characters"
        return content

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Retrieves the content of a specified file relative to the working directory, with a maximum character limit to prevent excessive output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to retrieve content from, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}