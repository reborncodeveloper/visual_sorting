from typing import TypedDict, Dict
from ast import parse, FunctionDef, FunctionType
from linecache import cache
from pathlib import Path
from json import loads, dumps

class Users_code(TypedDict):
    level_number : int
    level_data : Dict[int, int]
    time_spent : float 
    code : str
    
PAYLOAD_PATH = Path("/input/payload.json")
class FunctionNameError(Exception):
    pass
    
def run_key_function(code_path: Path, key_function_name: str = "sort"):
    with open(code_path, "r", encoding="utf-8") as file:
        users_data = loads(file.read())

    code = users_data["users_code"]
    array = list(users_data["level"]["items"])

    parsing_code = parse(code)
    functions = [i.name for i in parsing_code.body if isinstance(i, (FunctionDef, FunctionType))]
    if key_function_name not in functions:
        raise FunctionNameError

    namespace = {
        '__builtins__':
            {
                'range' : range,
                'len' : len,
                'enumerate' : enumerate,
                'int' : int,
                'str' : str,
                'list' : list,
                'tuple' : tuple,
                'dict' : dict,
                'zip' : zip,
                'min' : min,
                'max' : max
            }
    }

    cache['<user>'] = (
        len(code),
        None,
        [line + "\n" for line in code.splitlines()],
        '<user>',
    )
    
    exec(compile(parsing_code, '<user>', 'exec'), namespace)
    key_function = namespace[key_function_name]
    return key_function(array)



def main() -> None:
    try:
        result = list(run_key_function(PAYLOAD_PATH))
        users_data = loads(PAYLOAD_PATH.read_text(encoding="utf-8"))
        array = list(users_data["level"]["items"])
        ok = result == sorted(array) and len(result) == len(array)
        out = {"ok": ok, "result": result, "input": array, "expected_result" : sorted(array)}
    except Exception as e:
        out = {"ok": False, "error": str(e)}
    print(dumps(out, ensure_ascii=False), flush=True)
    
    
if __name__ == "__main__":
    main()