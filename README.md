# PipeBridge

The application is a simple communication interface for Windows between Rust and Python using Named Pipes. It provides an async Rust library and a standalone Python server to enable fast and reliable interprocess communication (IPC) for large payloads and structured messages.

---

## Features

- Async Rust library using Tokio for Named Pipe client
- Python server supporting length-prefixed message framing
- Reliable communication for payloads up to 5 MB
- JSON message support
- Fully Windows-compatible
- Example usage without GUI dependencies
- Easy integration with any Rust application or Tauri frontend

---

## Milestones

See the [Milestones.md](01-docs/Milestones.md) file for a task-level checklist to guide development from basic Rust ↔ Python communication to full JSON message support.

## License

See the [License](01-docs/LICENSE)
