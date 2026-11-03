import logging
from typing import Dict, TypedDict, List


logging.basicConfig(level=logging.INFO)

class Generated_level(TypedDict):
    name : str
    items : List[int]
    write_time_sec : float


async def generate_visual_part(generate_level : Generated_level) -> List[int]:
    input_list = generate_level['items']
    columns_height = [i*15 for i in input_list]
    return columns_height

