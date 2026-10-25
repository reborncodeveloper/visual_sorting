from typing import TypedDict, Dict
import ast
import linecache
import inspect

class Users_code(TypedDict):
    level_number : int
    level_data : Dict[int, int]
    time_spent : float 
    code : str
    
class FunctionNameError(Exception):
    pass
    
async def get_key_function(code : str, key_function_name : str = 'sort'):
    parsing_code = ast.parse(code)
    functions = [i.name for i in parsing_code.body if isinstance(i, (ast.FunctionDef, ast.FunctionType))]
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
    linecache.cache['<user>'] = (
        len(code),
        None,
        [line + "\n" for line in code.splitlines()],
        '<user>',
    )
    
    #compile
    exec(compile(parsing_code, '<user>', 'exec'), namespace)
    key_function = namespace[key_function_name]

    return key_function


    
def check_users_code(key_function) -> None:
    user_function = inspect.getsource(key_function)
    


if __name__ == "__main__":
    code = '\ndef sort():\n    "hello"\n'
    import asyncio
    async def main(code):
        key_function = await get_key_function(code)
        return await asyncio.to_thread(check_users_code, key_function)

    print(asyncio.run(main(code)))