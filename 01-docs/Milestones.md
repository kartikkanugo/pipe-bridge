# Pipe Bridge Milestones (Task-Level Checklist)

## Phase 1: Setup Rust IPC library

- [ ] Create Rust library crate `rust-client`
- [ ] Implement async Named Pipe client using Tokio
- [ ] Implement length-prefixed framing for messages
- [ ] Test sending/receiving small byte payloads locally
- [ ] Handle basic error cases (connection failures, broken pipe)

## Phase 2: Setup Python server

- [ ] Create Python Named Pipe server using `pywin32`
- [ ] Implement reading of length-prefixed messages from Rust
- [ ] Echo back received messages for initial testing
- [ ] Run server in a background thread or async loop
- [ ] Handle multiple consecutive connections

## Phase 3: Async integration

- [ ] Make Rust client fully async using Tokio
- [ ] Spawn multiple tasks to support concurrent requests
- [ ] Test Rust → Python → Rust roundtrip with small payloads
- [ ] Test large payloads (~5 MB)
- [ ] Add logging/debugging to trace message flow

## Phase 4: JSON messaging

- [ ] Implement JSON serialization in Rust using `serde_json`
- [ ] Send JSON payloads from Rust client to Python server
- [ ] Parse JSON in Python using `json` module
- [ ] Test sending complex structured JSON (nested objects, arrays)
- [ ] Validate integrity of JSON roundtrip

## Phase 5: Packaging

- [ ] Package Python server as a standalone binary using PyInstaller
- [ ] Ensure Rust client works with packaged Python server without Python installed
- [ ] Add example Rust integration with packaged server
- [ ] Document steps for building Python binary

## Phase 6: Validation & final goal

- [ ] Rust sends JSON file to Python → Python reads and prints/uses it
- [ ] Add integration tests for robustness and large payloads
- [ ] Add error handling for partial/failed transmissions
- [ ] Document usage examples in README
- [ ] ✅ Complete end-to-end test (Rust → Python JSON)
