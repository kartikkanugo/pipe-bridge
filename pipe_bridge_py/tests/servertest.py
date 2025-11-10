import asyncio
from pipe_bridge_py import PipeServer


async def main():
    server = PipeServer(r"\\.\pipe\test_pipe_123")
    try:
        await server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    asyncio.run(main())
