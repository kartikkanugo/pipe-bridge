import pipe_bridge_py

print(dir(pipe_bridge_py))
print("Module Imported successfully")
print(pipe_bridge_py.version)

import asyncio

async def sleep():
    result = await asyncio.sleep(10, result="hellow")
    print(result)


asyncio.run(sleep())