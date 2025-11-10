"""
Asynchronous Named Pipe Client for Windows.

- Connects to an existing named pipe server.
- Sends and receives messages asynchronously.
- Compatible with the PipeServer class implementation.
"""

import asyncio
import win32file
import win32pipe
import pywintypes
import time


class PipeClient:
    def __init__(self, pipe_name: str, buffer_size: int = 4096):
        self.pipe_name = pipe_name
        self.buffer_size = buffer_size
        self._handle = None
        self._loop = asyncio.get_running_loop()

    async def connect(self, timeout: int = 10):
        """
        Connect to the server's named pipe.

        Parameters:
            timeout (int): Time (in seconds) to wait for the server to appear.
        """
        start = time.time()
        print(f"[CLIENT] Connecting to {self.pipe_name} ...")

        while True:
            try:
                self._handle = win32file.CreateFile(
                    self.pipe_name,
                    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                    0,  # no sharing
                    None,
                    win32file.OPEN_EXISTING,
                    0,
                    None,
                )
                print("[CLIENT] Connected!")
                break
            except pywintypes.error as e:
                if e.args[0] != 2:  # ERROR_FILE_NOT_FOUND
                    raise
                if time.time() - start > timeout:
                    raise TimeoutError(f"[CLIENT] Timeout waiting for {self.pipe_name}")
                await asyncio.sleep(0.5)

    async def send_message(self, message: str):
        """
        Send a message to the server.

        Parameters:
            message (str): The message to send.
        """
        if not self._handle:
            raise RuntimeError("[CLIENT] Not connected to pipe.")

        await self._loop.run_in_executor(
            None, win32file.WriteFile, self._handle, message.encode()
        )
        print(f"[CLIENT] Sent: {message}")

    async def read_response(self):
        """
        Read the response from the server.
        """
        if not self._handle:
            raise RuntimeError("[CLIENT] Not connected to pipe.")

        try:
            result, data = await self._loop.run_in_executor(
                None, win32file.ReadFile, self._handle, self.buffer_size
            )
            msg = data.decode(errors="ignore").strip()
            print(f"[CLIENT] Received: {msg}")
            return msg
        except pywintypes.error as e:
            if e.args[0] == 109:  # ERROR_BROKEN_PIPE
                print("[CLIENT] Server disconnected.")
                return None
            raise

    def close(self):
        """Close the client pipe connection."""
        if self._handle:
            win32file.CloseHandle(self._handle)
            self._handle = None
            print("[CLIENT] Connection closed.")
