import logging
from typing import Dict, TypedDict, List
from math import log

logging.basicConfig(level=logging.INFO)

class Generated_level(TypedDict):
    name : str
    items : List[int]
    write_time_sec : float


async def generate_visual_part(generate_level : Generated_level) -> List[int]:
    input_list = generate_level['items']
    columns_height = [i*15 for i in input_list]
    return columns_height

def height_generator(input_list):
    return [int(-246.36 + 219.03 *(log(i + 3) / log(3))) for i in input_list]

def div_generator(input_list):
    columns_height = height_generator(input_list)
    return [f'<div class="test_column" style="height: {columns_height[i]}px;"><p>{input_list[i]}</p></div>' for i in range(len(columns_height)) ]
