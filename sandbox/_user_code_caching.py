from uuid import uuid4
from aiofiles import open
from uuid import UUID
from pathlib import Path 
from json import dumps

def generate_uuid() -> UUID:
    return uuid4()

async def create_user_cache(users_code : str, level : list) -> Path:
    uuid = generate_uuid()
    payload_data = {'users_code' : str(users_code), 'level' : level}
    cache_path = Path(f'./users_cache/runtime_inputs/{uuid}/payload.json')
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    async with open(cache_path, 'w+') as file:
        await file.write(dumps(payload_data))
    return cache_path