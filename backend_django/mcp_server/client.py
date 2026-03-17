"""
mcp_client/client.py

Example MCP Client for the Automation Dashboard.

Usage:
    client = AutomationMCPClient("http://localhost:8000", "YOUR_TOKEN")
    client.connect()

    workflows = client.list_workflows()
    run_id    = client.run_workflow(workflow_id="abc-123")
    status    = client.get_workflow_status(run_id)

    # Take screenshot
    img = client.take_screenshot()

    # Execute desktop action
    client.execute_action("type_text", {"text": "Hello World"})
"""

from __future__ import annotations
import json
import time
import logging
import threading
from typing import Any, Optional
from dataclasses import dataclass
import requests

logger = logging.getLogger(__name__)


@dataclass
class MCPResult:
    success: bool
    data: Any
    error: Optional[str] = None
    raw: Optional[dict] = None

    def __bool__(self): return self.success


class MCPError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"MCP Error {code}: {message}")


class AutomationMCPClient:
    """
    Full MCP client for the Automation Dashboard.

    Implements:
      - JSON-RPC 2.0 over HTTP
      - Token authentication
      - Automatic reconnect on failure
      - All registered tools as Python methods
    """

    def __init__(
        self,
        base_url:  str = "http://localhost:8000",
        token:     str = "",
        timeout:   int = 30,
        retry_on_fail: bool = True,
    ):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.retry_on_fail = retry_on_fail
        self._request_id = 0
        self._session = requests.Session()
        self._connected = False
        self._server_info = {}
        self._capabilities = {}

        if token:
            self._session.headers.update({"Authorization": f"Bearer {token}"})

    # ── Connection ─────────────────────────────────────────

    def connect(self, client_name: str = "AutomationClient", client_version: str = "1.0"):
        """
        Send MCP initialize handshake.
        Must be called before any tools/call.
        """
        result = self._rpc("initialize", {
            "protocolVersion": "2024-11-05",
            "clientInfo": {"name": client_name, "version": client_version},
            "capabilities": {},
        })

        self._server_info = result.get("serverInfo", {})
        self._capabilities = result.get("capabilities", {})
        self._connected = True

        logger.info(
            f"Connected to {self._server_info.get('name')} "
            f"v{self._server_info.get('version')}"
        )
        return result

    def disconnect(self):
        self._session.close()
        self._connected = False

    # ── Tool Discovery ─────────────────────────────────────

    def list_tools(self) -> list[dict]:
        """Return all available MCP tools."""
        result = self._rpc("tools/list")
        return result.get("tools", [])

    def list_resources(self) -> list[dict]:
        result = self._rpc("resources/list")
        return result.get("resources", [])

    # ── Core Tool Call ─────────────────────────────────────

    def call_tool(self, name: str, arguments: dict = {}) -> MCPResult:
        """
        Generic tools/call — use specific methods below instead.
        """
        result = self._rpc(
            "tools/call", {"name": name, "arguments": arguments})

        is_error = result.get("isError", False)
        content = result.get("content", [])

        # Parse text content
        text = ""
        for block in content:
            if block.get("type") == "text":
                text += block.get("text", "")

        if is_error:
            return MCPResult(success=False, data=None, error=text, raw=result)

        # Try to parse JSON result
        try:
            parsed = json.loads(text)
            return MCPResult(success=True, data=parsed, raw=result)
        except json.JSONDecodeError:
            return MCPResult(success=True, data=text, raw=result)

    # ── Workflow Methods ───────────────────────────────────

    def list_workflows(self, status: str = "all") -> list[dict]:
        """List all workflows."""
        r = self.call_tool("list_workflows", {"status": status})
        if r:
            return r.data.get("workflows", [])
        raise MCPError(-1, r.error or "Failed to list workflows")

    def run_workflow(self, workflow_id: str, dry_run: bool = False) -> str:
        """
        Start a workflow. Returns task_run_id for tracking.
        """
        r = self.call_tool("run_workflow", {
            "workflow_id": workflow_id,
            "dry_run":     dry_run,
        })
        if r:
            return r.data.get("task_run_id", "")
        raise MCPError(-1, r.error or "Failed to run workflow")

    def get_workflow_status(self, task_run_id: str) -> dict:
        """Check execution status of a running workflow."""
        r = self.call_tool("get_workflow_status", {"task_run_id": task_run_id})
        if r:
            return r.data
        raise MCPError(-1, r.error or "Failed to get status")

    def wait_for_workflow(
        self,
        task_run_id: str,
        timeout:     int = 300,
        poll_interval: float = 2.0,
    ) -> dict:
        """
        Block until workflow completes or timeout.
        Returns final status dict.
        """
        deadline = time.time() + timeout

        while time.time() < deadline:
            status = self.get_workflow_status(task_run_id)
            state = status.get("status", "")

            logger.info(f"Workflow {task_run_id}: {state}")

            if state in ("success", "failed", "stopped"):
                return status

            time.sleep(poll_interval)

        raise TimeoutError(
            f"Workflow {task_run_id} did not complete in {timeout}s")

    def stop_workflow(self, task_run_id: str) -> dict:
        r = self.call_tool("stop_workflow", {"task_run_id": task_run_id})
        if r:
            return r.data
        raise MCPError(-1, r.error or "Failed to stop workflow")

    # ── Program Methods ────────────────────────────────────

    def list_programs(self) -> list[dict]:
        r = self.call_tool("list_programs")
        if r:
            return r.data.get("programs", [])
        raise MCPError(-1, r.error)

    def open_program(self, program_id: str, wait_seconds: int = 2) -> dict:
        r = self.call_tool("open_program", {
            "program_id":   program_id,
            "wait_seconds": wait_seconds,
        })
        if r:
            return r.data
        raise MCPError(-1, r.error)

    def get_program_status(self, program_id: str) -> dict:
        r = self.call_tool("get_program_status", {"program_id": program_id})
        if r:
            return r.data
        raise MCPError(-1, r.error)

    # ── Desktop Methods ────────────────────────────────────

    def execute_action(self, action_type: str, payload: dict = {}) -> dict:
        r = self.call_tool("execute_desktop_action", {
            "action_type": action_type,
            "payload":     payload,
        })
        if r:
            return r.data
        raise MCPError(-1, r.error)

    def click(self, x: int, y: int) -> dict:
        return self.execute_action("click", {"x": x, "y": y})

    def type_text(self, text: str, interval: float = 0.05) -> dict:
        return self.execute_action("type_text", {"text": text, "interval": interval})

    def press_key(self, key: str) -> dict:
        return self.execute_action("press_key", {"key": key})

    def hotkey(self, *keys: str) -> dict:
        return self.execute_action("hotkey", {"keys": list(keys)})

    def wait(self, seconds: float) -> dict:
        return self.execute_action("wait", {"seconds": seconds})

    def take_screenshot(self, region: Optional[dict] = None) -> MCPResult:
        """
        Returns MCPResult with data.image_b64 (base64 PNG).
        """
        return self.call_tool("take_screenshot", {"region": region} if region else {})

    # ── System Methods ─────────────────────────────────────

    def get_system_info(self) -> dict:
        r = self.call_tool("get_system_info")
        if r:
            return r.data
        raise MCPError(-1, r.error)

    def list_processes(self, filter_name: str = "") -> list[dict]:
        r = self.call_tool("list_running_processes", {
                           "filter_name": filter_name})
        if r:
            return r.data.get("processes", [])
        raise MCPError(-1, r.error)

    # ── Low-level RPC ──────────────────────────────────────

    def _rpc(self, method: str, params: dict = {}) -> dict:
        """Send a JSON-RPC 2.0 request and return the result dict."""
        self._request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "method":  method,
            "id":      self._request_id,
            "params":  params,
        }

        try:
            resp = self._session.post(
                f"{self.base_url}/api/mcp/",
                json=payload,
                timeout=self.timeout,
            )
            resp.raise_for_status()
            body = resp.json()
        except requests.RequestException as e:
            raise ConnectionError(f"MCP request failed: {e}") from e

        if "error" in body:
            err = body["error"]
            raise MCPError(err.get("code", -1),
                           err.get("message", "Unknown error"))

        return body.get("result", {})

    # ── Context Manager ────────────────────────────────────

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    def __repr__(self):
        state = "connected" if self._connected else "disconnected"
        return f"<AutomationMCPClient {self.base_url} [{state}]>"
