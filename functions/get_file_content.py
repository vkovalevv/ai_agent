import os 
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
MAX_CHARS = int(os.getenv("MAX_CHARS"))

def get_file_content(working_directory: str, file_path: str) -> str:
    absolute_path = os.path.abspath(working_directory)
    file_path = os.path.normpath(os.path.join(absolute_path,file_path)) 

    valid_target_file = os.path.commonpath([absolute_path, file_path]) == absolute_path

    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(file=file_path,mode='r') as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += f'[...file "{file_path}" truncated at {MAX_CHARS} characters'
    except Exception as e:
        return f'  Error: {e}'

    return content


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns the text contents of a file. The file path must be relative to the configured working directory.",
        "parameters":{
            "type":"object",
            "properties": {
                "file_path": {
                    "type":"string",
                    "description": "Relative path to the file within the configured working directory, for example 'main.py' or 'pkg/render.py'.",
                }
            }
        }
    }
}