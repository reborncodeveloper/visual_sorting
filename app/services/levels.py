from typing import TypedDict, Dict
import random
import aiofiles
import json
from pathlib import Path

LEVELS_DIR = Path('data/levels_configs')

class Level_Data(TypedDict):
    name : str
    items_in_list : int
    wright_time_sec : float
    column_range : int
    
class Generated_level(TypedDict):
    name : str
    items : Dict[int, int]
    wright_time_sec : float

async def get_level_data(level_number : int) -> Level_Data:
    level_path = LEVELS_DIR / f'level{level_number}.json'
    async with aiofiles.open(level_path) as file:
        raw_level_data = await file.read()
    
    level_data = json.loads(raw_level_data)
    
    return Level_Data(
        name=level_data["name"],
        items_in_list=level_data["items_in_list"],
        wright_time_sec=level_data["wright_time_sec"],
        column_range=level_data["column_range"]
    )


async def generate_level(level_data : Level_Data) -> Generated_level:
    name : str = level_data['name']
    wright_time_sec : float = level_data['wright_time_sec']
    items_in_list : int = level_data['items_in_list']
    column_range : int = level_data['column_range']
    
    items : Dict[int, int] = {}
    for i in range(items_in_list):
        items[i] = random.randint(0, column_range)
        
    return Generated_level(name=name, items=items, wright_time_sec=wright_time_sec)

        
