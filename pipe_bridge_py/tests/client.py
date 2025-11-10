import asyncio
import win32file
import win32pipe
import pywintypes

PIPE_NAME = r"\\.\pipe\test_pipe_123"
BUFFER_SIZE = 4096


async def send_messages():
    """Connect to server and send messages"""
    print(f"[CLIENT] Connecting to {PIPE_NAME}...")

    try:
        # Wait for pipe to be available
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, win32pipe.WaitNamedPipe, PIPE_NAME, 5000  # 5 second timeout
        )

        # Open the pipe
        pipe_handle = win32file.CreateFile(
            PIPE_NAME,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None,
        )

        # Set message read mode
        win32pipe.SetNamedPipeHandleState(
            pipe_handle, win32pipe.PIPE_READMODE_MESSAGE, None, None
        )

        print("[CLIENT] Connected to server!")

        # Send some test messages
        messages = [
            "Hello, Server!",
            "How are you?",
            "Testing Named Pipes on Windows",
            "Goodbye!",
        ]

        for msg in messages:
            print(f"[CLIENT] Sending: {msg}")

            # Write to pipe
            win32file.WriteFile(pipe_handle, msg.encode())

            # Read response
            result, data = win32file.ReadFile(pipe_handle, BUFFER_SIZE)
            response = data.decode()
            print(f"[CLIENT] Received: {response}")

            # Small delay between messages
            await asyncio.sleep(1)

        # Close pipe
        win32file.CloseHandle(pipe_handle)
        print("[CLIENT] Connection closed")

    except pywintypes.error as e:
        if e.args[0] == 2:  # ERROR_FILE_NOT_FOUND
            print("[CLIENT] Error: Could not connect to server. Is the server running?")
        else:
            print(f"[CLIENT] Error: {e}")
    except Exception as e:
        print(f"[CLIENT] Error: {e}")


async def main():
    await send_messages()


if __name__ == "__main__":
    asyncio.run(main())
