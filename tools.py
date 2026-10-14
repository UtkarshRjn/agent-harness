tools = [{
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "This is a bash tool that can be used to read file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to read"
                }
            },
            "required": ["path"]
        }
    }
}]

def read_file(path: str):

    with open(path, 'r') as file:
        content = file.read()
    
    return content