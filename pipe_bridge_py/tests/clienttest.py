import asyncio
from pipe_bridge_py import PipeClient


async def main():

    client = PipeClient(r"\\.\pipe\test_pipe_123")

    await client.connect()

    for i in range(3):
        msg = f"Hello {i}"
        await client.send_message(msg)
        await asyncio.sleep(0.1)
        await client.read_response()

    client.close()


if __name__ == "__main__":
    asyncio.run(main())
