import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(absolute_path,file_path)) 
        
        valid_target_file = os.path.commonpath([absolute_path, abs_file_path]) == absolute_path

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        _, file_ext = os.path.splitext(file_path)

        if file_ext != '.py':
            return f'Error "{file_path}" is not a Python file.'

        command = ['python', abs_file_path]

        if args:
            command.extend(args)

        subprocess_result = subprocess.run(command, text=True, timeout=30.0, capture_output=True)

        completedprocess_string = ''
        if subprocess_result.returncode != 0:
            completedprocess_string += f'Process exited with code {subprocess_result.returncode}'

        if subprocess_result.stderr is None and subprocess_result.stdout is None:
            completedprocess_string += 'No output produced'
        else:
            if subprocess_result.stdout:
                completedprocess_string += 'STDOUT: ' + subprocess_result.stdout
            if subprocess_result.stderr:
                completedprocess_string += 'STDERR: ' + subprocess_result.stderr

        return completedprocess_string
    
    except Exception as e:
        return f'Error: executing python file: {e}'    

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a file with the .py extension",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file with the .py extension is relative to the working directory.",
                },
                "args":{
                    "type": "array",
                    "items": {"type":"string"},
                    "description": "Parameters passed to the function of the launched subprocess."
                }
            },
        },
    },
}
