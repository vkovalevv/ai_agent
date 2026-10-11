import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        file_path =  os.path.normpath(os.path.join(absolute_path,file_path))

        valid_file_path = os.path.commonpath([absolute_path, file_path]) == absolute_path

        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

        with open(file_path, mode='w') as f:
            f.write(content)
    except Exception as e:
        return f' Error: {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes `info` to `file`, relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "Content that is written to a file."
                }
            },
        },
    },
}
