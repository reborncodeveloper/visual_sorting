from typing import TypedDict, Dict
from ast import parse, FunctionDef, FunctionType
from linecache import cache
from inspect import getsource
from sandbox._user_code_caching import create_user_cache
from pathlib import Path
from subprocess import run
class Users_code(TypedDict):
    level_number : int
    level_data : Dict[int, int]
    time_spent : float 
    code : str
    
class FunctionNameError(Exception):
    pass
    
async def get_key_function(code : str, key_function_name : str = 'sort'):
    parsing_code = parse(code)
    functions = [i.name for i in parsing_code.body if isinstance(i, (FunctionDef, FunctionType))]
    if not key_function_name in functions:
        raise FunctionNameError
    
    
    #maintain namespace to avoid functions and imports in code
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
    
    #caching lines specially for inspect
    cache['<user>'] = (
        len(code),
        None,
        [line + "\n" for line in code.splitlines()],
        '<user>',
    )
    
    #compile
    exec(compile(parsing_code, '<user>', 'exec'), namespace)
    key_function = namespace[key_function_name]

    return key_function


    
async def get_users_code_path(key_function, level) -> Path:
    user_function_code = getsource(key_function)
    return await create_user_cache(user_function_code, level)
    
# async def run_users_code(user_code_path : Path):
#     run('''docker run --rm \
#   --network none \
#   --memory 64m \
#   --cpus 0.5 \
#   --pids-limit 64 \
#   --read-only \
#   --tmpfs /tmp:rw,noexec,nosuid,size=16m \
#   --user 10001:10001 \
#   --cap-drop ALL \
#   --security-opt no-new-privileges \
#   -v "$PWD/users_cache/runtime_inputs/2ee1a74a-be4e-4a5b-8281-2a6619257f89:/input:ro" \
#   visual-sorting-sandbox''', shell=True)


