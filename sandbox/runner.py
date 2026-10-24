from typing import TypedDict, Dict
import ast

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
    
    exec(compile(parsing_code, '<user>', 'exec'), namespace)
    key_function = namespace[key_function_name]

    return namespace


async def check_users_code(key_function : str) -> None:
    ...
    
    
if __name__ == '__main__':
    import asyncio
    code = '''
def sort():
    print("hello")
'''
    async def main(code):
        return await get_key_function(code)
    
    print(asyncio.run(main(code)))