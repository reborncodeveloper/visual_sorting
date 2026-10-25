from uuid import uuid4
from aiofiles import open
from uuid import UUID
from pathlib import Path 

def generate_uuid() -> UUID:
    return uuid4()

async def create_user_cache(users_code : str) -> Path:
    uuid = generate_uuid()
    cache_path = Path(f'./users_cache/runtime_inputs/{uuid}/payload.json')
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    async with open(cache_path, 'w+') as file:
        await file.write(users_code)
    return cache_path