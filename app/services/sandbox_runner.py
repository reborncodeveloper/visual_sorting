from typing import TypedDict, Dict
from ast import parse, FunctionDef, FunctionType
from linecache import cache
from inspect import getsource
from services._user_code_caching import create_user_cache
from pathlib import Path
import asyncio
import logging
import shutil

logging.basicConfig(level=logging.INFO)

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

    return key_function


    
async def get_users_code_path(users_code: str, level) -> Path:
    return await create_user_cache(users_code, level)


async def run_users_code(users_code_dir: Path) -> str:
    abs_dir = str(users_code_dir.parent.resolve()) 
    logging.info("mount dir: %s", abs_dir)
    logging.info("payload exists: %s", Path(abs_dir, "payload.json").exists())

    proc = await asyncio.create_subprocess_exec(
        "docker", "run", "--rm",
        "--network", "none",
        "--memory", "64m",
        "--cpus", "0.5",
        "--pids-limit", "64",
        "--read-only",
        "--tmpfs", "/tmp:rw,noexec,nosuid,size=16m",
        "--user", "10001:10001",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "-v", f"{abs_dir}:/input:ro",
        "visual-sorting-sandbox",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=3)
    if proc.returncode != 0:
        raise RuntimeError(stderr.decode()[:500])
    
    shutil.rmtree(abs_dir) 
    return stdout.decode()