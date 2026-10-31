import pytest
from sandbox.runner import run_key_function
import logging

logging.basicConfig(level=logging.INFO)

@pytest.mark.parametrize('path',['users_cache/runtime_inputs/a7afee1c-1a04-4ec7-a747-8058668324f0/payload.json', 'users_cache/runtime_inputs/6be35579-5e27-4d8a-b0c8-98ffa602c452/payload.json'])
async def test_run_key_function(path):
    result = await run_key_function(path)
    logging.info(result)
    
    assert result
