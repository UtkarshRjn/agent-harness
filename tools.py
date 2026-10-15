import json

tools = [{
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "This is a file read tool that can be used to read file if we provide it with a path",
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
},{
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write content to a file at the given path. Creates the file if it does not exist, overwrites if it does.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to write"
                },
                "content": {
                    "type": "string",
                    "description": "Content that needs to be written in the file"
                },
            },
            "required": ["path", "content"]
        }
    }
}]

def read_file(path: str) -> str:

    with open(path, 'r') as file:
        content = file.read()
    
    return content

def write_file(path: str, content: str) -> str:
    with open(path, "w") as file:
        file.write(content)
    
    return f"Wrote {len(content)} characters to {path}"

def execute(tool_call):

    tool_name = tool_call["function"]["name"]
    print("Tool Call:", tool_name)
    
    if tool_name not in TOOL_REGISTRY:
        content = "Error: unknown tool: " + tool_name
    else:
        try:
            args = json.loads(tool_call["function"]["arguments"])
            content = TOOL_REGISTRY[tool_name](**args)
        except Exception as e:
            content = f"Tool error: {e}"
    
    return content

TOOL_REGISTRY = {
    "read_file": read_file,
    "write_file": write_file,
}
