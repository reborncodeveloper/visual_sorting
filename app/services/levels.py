from typing import TypedDict, List
from random import randint
from aiofiles import open
from json import loads
from pathlib import Path

LEVELS_DIR = Path('data/levels_configs')

class Level_Data(TypedDict):
    name : str
    items_in_list : int
    write_time_sec : float
    column_range : int
    
class Generated_level(TypedDict):
    name : str
    items : List[int]
    write_time_sec : float

async def get_level_data(level_number : int) -> Level_Data:
    level_path = LEVELS_DIR / f'level{level_number}.json'
    async with open(level_path) as file:
        raw_level_data = await file.read()
    
    level_data = loads(raw_level_data)
    
    return Level_Data(
        name=level_data["name"],
        items_in_list=level_data["items_in_list"],
        write_time_sec=level_data["write_time_sec"],
        column_range=level_data["column_range"]
    )


async def generate_level(level_data : Level_Data) -> Generated_level:
    name : str = level_data['name']
    write_time_sec : float = level_data['write_time_sec']
    items_in_list : int = level_data['items_in_list']
    column_range : int = level_data['column_range']
    
    items : List[int] = list()
    #here we crate level but I guess I will change it because if we have only 1 test user can just write return [...,...,...] in right sequence
    #but also we can check if time of program work is 0 we just print that user cheated and it is not fair something like that
    for i in range(items_in_list):
        items.append(randint(0, column_range))
        
    return Generated_level(name=name, items=items, write_time_sec=write_time_sec)

