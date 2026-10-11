import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
MAX_CHARS = os.getenv("MAX_CHARS")


def get_files_info(working_directory: str, directory: str = ".") -> str:
    absolute_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_path, directory))

    valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

    if not valid_target_dir:
        return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'   Error: "{directory}" is not a directory'

    dir_content = list(Path(target_dir).iterdir())

    content = ""
    for file in dir_content:
        content += f" - {os.path.relpath(file, target_dir)}, file_size={file.stat().st_size}, is_dir={file.is_dir()}\n"

    return content


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists the immediate entries in a directory, returning each entry's name, size in bytes, and whether it is a directory. The directory path must be relative to the configured working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Relative path to the directory to inspect, for example '.' for the configured working directory or 'pkg' for a subdirectory. If omitted, the configured working directory is used.",
                },
            },
        },
    },
}
