import jinja2
import aiohttp_jinja2
from aiohttp import web
from services.levels import generate_level, get_level_data
from services.visual import div_generator
from services.sandbox_runner import get_users_code_path, run_users_code, get_key_function
import logging
from json import loads

logging.basicConfig(level=logging.INFO)
app = web.Application()

aiohttp_jinja2.setup(
    app, 
    loader=jinja2.FileSystemLoader('templates')
    
)
app.router.add_static('/static/', path='static', name='static')


#just for test not hardcode
level_number = 1


@aiohttp_jinja2.template('index.html')
async def index(request):
    
    level_data = await get_level_data(level_number)
    generated_level = await generate_level(level_data)
    columns = div_generator(generated_level['items'])
    return { 'columns' : columns,  'level': generated_level}


async def run_code(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "error": "invalid json"}, status=400)
    users_code = data.get("code")
    level = data.get("level") 
    if not isinstance(users_code, str) or not users_code.strip():
        return web.json_response({"ok": False, "error": "code is required"}, status=400)
    if not isinstance(level, dict) or "items" not in level:
        return web.json_response({"ok": False, "error": "level is required"}, status=400)
    try:
        users_code_path = await get_users_code_path(users_code, level)
        
        logging.info(users_code_path)
    except Exception as e:
        logging.exception(e)
        return web.json_response({"ok": False, "error": "unexpected error"}, status=400)
    try:
        raw = await run_users_code(users_code_path) 
        payload = loads(raw)
        return web.json_response(payload)
    except Exception as e:
        logging.exception(e)
        return web.json_response({"ok": False, "error": "code error"}, status=400)


app.router.add_get('/', index)
app.router.add_post('/api/run', run_code)

web.run_app(app, port=1024)


# <div class="test_column" style="height: 50px; "><p>2</p></div>