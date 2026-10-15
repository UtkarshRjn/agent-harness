import json

"""
We are adding offest and limit to file read so that large files that don't fit into the context memory can also be read by an agent one by one.
"""

tools = [{
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read a slice of a file. Returns one header line 'start-end/total' then the text. Use offset and limit to page through large files.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to read"
                },
                "offset": {
                    "type": "integer",
                    "description": "The offset value from where you want to read"
                },
                "limit": {
                    "type": "integer",
                    "description": "Numer of charcters in the file you want to read"
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

MAX_CONTENT_SIZE = 8000 # Won't give more than 8000 characters to an agent

def read_file(path: str, offset: int = 0, limit: int = 1000) -> str:

    with open(path, "r") as file:
        file.seek(0, 2)
        total = file.tell()

        if offset > total:
            offset = total
        
        file.seek(offset)
        content = file.read(limit)

    end = offset + len(content)
    return f"Header: {offset}-{end}/{total} \n Content: {content}"

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
    
    if len(content) >= MAX_CONTENT_SIZE:
        content = content[:MAX_CONTENT_SIZE] + f"\n(truncated, original {len(content)} chars)"

    return content

TOOL_REGISTRY = {
    "read_file": read_file,
    "write_file": write_file,
    "str_replace": str_replace,
}
