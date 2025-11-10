import asyncio
import win32pipe
import win32file
import pywintypes

PIPE_NAME = r"\\.\pipe\test_pipe_123"
BUFFER_SIZE = 4096


async def handle_client(pipe_handle):
    """Handle a client connection"""
    print("[SERVER] Client connected")

    try:
        while True:
            # Read from pipe
            result, data = win32file.ReadFile(pipe_handle, BUFFER_SIZE)

            if not data:
                print("[SERVER] Client disconnected")
                break

            message = data.decode()
            print(f"[SERVER] Received: {message}")

            # Write response
            response = f"Echo: {message}"
            win32file.WriteFile(pipe_handle, response.encode())
            print(f"[SERVER] Sent: {response}")

    except pywintypes.error as e:
        if e.args[0] == 109:  # ERROR_BROKEN_PIPE
            print("[SERVER] Client disconnected (pipe broken)")
        else:
            print(f"[SERVER] Error: {e}")
    finally:
        win32file.CloseHandle(pipe_handle)
        print("[SERVER] Connection closed")


async def accept_client():
    """Accept a single client connection"""
    # Create named pipe
    pipe_handle = win32pipe.CreateNamedPipe(
        PIPE_NAME,
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE
        | win32pipe.PIPE_READMODE_MESSAGE
        | win32pipe.PIPE_WAIT,
        1,  # Max instances
        BUFFER_SIZE,
        BUFFER_SIZE,
        0,  # Default timeout
        None,
    )

    print("[SERVER] Waiting for client connection...")

    # Wait for client to connect (blocking call, run in executor)
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, win32pipe.ConnectNamedPipe, pipe_handle, None)

    # Handle client in background
    await handle_client(pipe_handle)


async def main():
    print(f"[SERVER] Starting server on {PIPE_NAME}")

    while True:
        try:
            await accept_client()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[SERVER] Error: {e}")
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SERVER] Server stopped by user")
