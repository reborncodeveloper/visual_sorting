import pytest
from sandbox.runner import main
import asyncio
import logging

#uv run pytest -v --log-cli-level=INFO tests/test_runner.py 
#for tests

logging.basicConfig(level=logging.INFO)

def test_main():
    result = asyncio.run(main())
    logging.info(result)
    assert result