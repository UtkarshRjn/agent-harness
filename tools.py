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
},
{
    "type": "function",
    "function": {
        "name": "str_replace",
        "description": "Replace a string with another string in a file with the given path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file wherein we want to replace string"
                },
                "old_string": {
                    "type": "string",
                    "description": "Original string in the file"
                },
                "new_string": {
                    "type": "string",
                    "description": "New string in the file"
                }
            },
            "required": ["path", "old_string", "new_string"]
        }
    }
}
]

def read_file(path: str) -> str:

    with open(path, 'r') as file:
        content = file.read()
    
    return content

def write_file(path: str, content: str) -> str:
    with open(path, "w") as file:
        file.write(content)
    
    return f"Wrote {len(content)} characters to {path}"

def str_replace(path: str, old_string: str, new_string: str) -> str:
    with open(path, "r") as file:
        content = file.read()
    
    if not old_string:
        return "Please provide correct string to replace"

    match_count = content.count(old_string)

    if match_count == 1:
        updated_content = content.replace(old_string, new_string)
        with open(path, "w") as file:
            file.write(updated_content)
        return f"Replaced {old_string} with {new_string} in {path}"
    elif match_count == 0:
        return f"{old_string} not found in {path}"
    
    return f"{old_string} found {match_count} times in {path}. Please replace a unique string."

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
    "str_replace": str_replace,
}
