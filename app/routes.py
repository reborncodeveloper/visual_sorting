import jinja2
import aiohttp_jinja2
from aiohttp import web
from math import log
from services.levels import generate_level, get_level_data

app = web.Application()

aiohttp_jinja2.setup(
    app, 
    loader=jinja2.FileSystemLoader('templates')
    
)
app.router.add_static('/static/', path='static', name='static')


def height_generator(input_list):
    return [int(-246.36 + 219.03 *(log(i + 3) / log(3))) for i in input_list]

def div_generator(input_list):
    columns_height = height_generator(input_list)
    return [f'<div class="test_column" style="height: {columns_height[i]}px;"><p>{input_list[i]}</p></div>' for i in range(len(columns_height)) ]

@aiohttp_jinja2.template('index.html')
async def index(request):
    #just for test not hardcode
    level_number = 1
    level_data = await get_level_data(level_number)
    generated_level = await generate_level(level_data)
    columns = div_generator(generated_level['items'])
    return { 'columns' : columns}

app.router.add_get('/', index)
web.run_app(app, port=1024)


# <div class="test_column" style="height: 50px; "><p>2</p></div>