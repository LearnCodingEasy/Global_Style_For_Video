"""
mcp_server/protocol.py

MCP Protocol Implementation (JSON-RPC 2.0 over HTTP)
Spec: https://spec.modelcontextprotocol.io

Supported methods:
  initialize          → server info + capabilities
  tools/list          → list registered tools
  tools/call          → execute a tool
  resources/list      → list available resources
  prompts/list        → list prompt templates
"""

from __future__ import annotations
import json
import uuid
import logging
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────
# Protocol Types
# ──────────────────────────────────────────────────────────

@dataclass
class MCPError:
    code: int
    message: str
    data: Optional[Any] = None

    # Standard JSON-RPC error codes
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603

    # MCP-specific codes
    TOOL_NOT_FOUND = -32000
    TOOL_ERROR = -32001
    AUTH_REQUIRED = -32002
    RATE_LIMITED = -32003


@dataclass
class MCPRequest:
    jsonrpc: str
    method: str
    id: Optional[str | int] = None
    params: Optional[dict] = None

    @classmethod
    def from_dict(cls, data: dict) -> "MCPRequest":
        return cls(
            jsonrpc=data.get("jsonrpc", "2.0"),
            method=data.get("method", ""),
            id=data.get("id"),
            params=data.get("params") or {},
        )


@dataclass
class MCPResponse:
    jsonrpc: str = "2.0"
    id: Optional[str | int] = None
    result: Optional[Any] = None
    error: Optional[dict] = None

    def to_dict(self) -> dict:
        d = {"jsonrpc": self.jsonrpc, "id": self.id}
        if self.error is not None:
            d["error"] = self.error
        else:
            d["result"] = self.result
        return d

    @classmethod
    def success(cls, id, result) -> "MCPResponse":
        return cls(id=id, result=result)

    @classmethod
    def error(cls, id, code: int, message: str, data=None) -> "MCPResponse":
        err = {"code": code, "message": message}
        if data is not None:
            err["data"] = data
        return cls(id=id, error=err)


# ──────────────────────────────────────────────────────────
# Tool Schema
# ──────────────────────────────────────────────────────────

@dataclass
class ToolParameter:
    name: str
    type: str          # string | number | boolean | object | array
    description: str
    required: bool = True
    enum: Optional[list] = None
    default: Optional[Any] = None


@dataclass
class MCPTool:
    name: str
    description: str
    parameters: list[ToolParameter]
    handler: Callable
    category: str = "general"
    enabled: bool = True
    require_auth: bool = True

    def to_schema(self) -> dict:
        """Return JSON Schema representation for MCP tools/list"""
        props = {}
        required = []

        for p in self.parameters:
            prop = {"type": p.type, "description": p.description}
            if p.enum:
                prop["enum"] = p.enum
            if p.default is not None:
                prop["default"] = p.default
            props[p.name] = prop
            if p.required:
                required.append(p.name)

        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": {
                "type": "object",
                "properties": props,
                "required": required,
            },
        }
