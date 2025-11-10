import asyncio
import time


def blocking_task(x):
    print(f"Task started: {x}\n", flush=True)
    time.sleep(1)
    print(f"Task finished: {x}\n", flush=True)
    print(f"Task finished: {x}\n", flush=True)
    return x * 2


async def main():
    loop = asyncio.get_running_loop()
    future = loop.run_in_executor(None, blocking_task, 5)  # starts immediately
    print("After run_in_executor, before await \n", flush=True)
    time.sleep(2)
    print("sleep running ", flush=True)
    result = await future  # waits here until task completes
    print("Got result:", result, flush=True)


asyncio.run(main())
