"""
Single-pipe async server using Windows Named Pipe.

Design:
- Creates one named pipe once.
- Waits for a client connection (blocking, done in executor).
- Reads messages continuously from that one pipe.
- Offloads CPU-heavy work to a single process via ProcessPoolExecutor.
- Gracefully shuts down on stop().
"""

import asyncio
import time
import pywintypes
import win32pipe
import win32file
from concurrent.futures import ProcessPoolExecutor


class PipeServer:
    def __init__(self, pipe_name: str, buffer_size: int = 4096):
        self.pipe_name = pipe_name
        self.buffer_size = buffer_size
        self._queue = asyncio.Queue()
        self._shutdown_event = asyncio.Event()
        self._executor = ProcessPoolExecutor(max_workers=1)
        self._pipe_handle = None

    async def start(self):
        """Start the server — create pipe once, wait for one client, read forever."""
        print(f"[SERVER] Starting on {self.pipe_name}")
        self._shutdown_event.clear()

        # Create pipe only once
        self._pipe_handle = win32pipe.CreateNamedPipe(
            self.pipe_name,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE
            | win32pipe.PIPE_READMODE_MESSAGE
            | win32pipe.PIPE_WAIT,
            1,  # Max one client
            self.buffer_size,
            self.buffer_size,
            0,
            None,
        )

        # Wait for client connection (blocking)
        loop = asyncio.get_running_loop()
        print("[SERVER] Waiting for client connection...")
        await loop.run_in_executor(
            None, win32pipe.ConnectNamedPipe, self._pipe_handle, None
        )
        print("[SERVER] Client connected")

        # Start worker in background
        worker_task = asyncio.create_task(self._math_worker())

        try:
            await self._handle_client()
        finally:
            await self._queue.join()
            worker_task.cancel()
            win32file.CloseHandle(self._pipe_handle)
            print("[SERVER] Server stopped cleanly")

    async def _handle_client(self):
        """Continuously read from one connected client."""
        while not self._shutdown_event.is_set():
            try:
                result, data = win32file.ReadFile(self._pipe_handle, self.buffer_size)

                if not data:
                    print("[SERVER] No data, waiting...")
                    await asyncio.sleep(0.05)
                    continue

                message = data.decode(errors="ignore").strip()
                print(f"[SERVER] Received: {message}")
                await self._queue.put(message)

                # optional: echo back
                response = f"ACK: {message}"
                win32file.WriteFile(self._pipe_handle, response.encode())

            except pywintypes.error as e:
                if e.args[0] == 109:  # ERROR_BROKEN_PIPE
                    print("[SERVER] Client disconnected (pipe broken)")
                    break
                else:
                    print(f"[SERVER] Error: {e}")
                    await asyncio.sleep(0.1)

    async def _math_worker(self):
        """Single process worker to handle heavy math in background."""
        loop = asyncio.get_running_loop()
        while not self._shutdown_event.is_set():
            try:
                data = await self._queue.get()
            except asyncio.CancelledError:
                break

            await loop.run_in_executor(self._executor, self._heavy_math, data)
            self._queue.task_done()

    @staticmethod
    def _heavy_math(data):
        """Simulate CPU-heavy processing."""
        time.sleep(1)
        print(f"[WORKER] Processed: {data}")

    def stop(self):
        """Trigger graceful shutdown."""
        print("[SERVER] Shutdown requested...")
        self._shutdown_event.set()
