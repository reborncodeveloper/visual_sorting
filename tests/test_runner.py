import pytest
from sandbox.runner import get_key_function, get_users_code_path
from app.services.levels import generate_level, get_level_data

import asyncio
import logging
import os

#uv run pytest -v --log-cli-level=INFO tests/test_runner.py 
#for tests

logging.basicConfig(level=logging.INFO)


@pytest.fixture(params=[1])
async def level_data(request):
    level_number = request.param
    level_data = await get_level_data(level_number)
    logging.info(level_data)
    assert level_data
    return level_data


@pytest.fixture
async def level(level_data):
    level = await generate_level(level_data)
    logging.info(level)
    assert level
    return level


@pytest.fixture(params=[
    '\ndef sort():\n    "hello"\n',
    '\ndef not_sort():\n    "hello"\n',
    '\ndef sort():\n    None\n',
    'print()'
])
async def key_function(request):
    code = request.param
    key_function = await get_key_function(code)
    logging.info(code)
    assert key_function
    return key_function


async def test_get_users_code_path(key_function, level):
    users_code_path = await get_users_code_path(key_function, level)
    logging.info(users_code_path)
    assert os.path.exists(users_code_path)