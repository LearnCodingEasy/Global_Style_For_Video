"""
mcp_server/registry.py

Central Tool Registry for MCP Server.

Usage:
    from mcp_server.registry import tool_registry

    @tool_registry.register(
        name="run_workflow",
        description="Execute a workflow",
        parameters=[...],
        category="workflows",
    )
    def run_workflow_handler(params, user):
        ...
"""

from __future__ import annotations
import logging
from typing import Any, Callable, Optional
from .protocol import MCPTool, ToolParameter

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Singleton registry for all MCP tools.
    Maps tool names → MCPTool objects.
    """

    _instance: Optional["ToolRegistry"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools: dict[str, MCPTool] = {}
            cls._instance._usage_stats: dict[str, int] = {}
        return cls._instance

    # ── Registration ──────────────────────────────────────

    def register(
        self,
        name: str,
        description: str,
        parameters: list[dict],
        category: str = "general",
        require_auth: bool = True,
    ):
        """Decorator factory — registers a function as an MCP tool."""

        def decorator(fn: Callable) -> Callable:
            params = [
                ToolParameter(
                    name=p["name"],
                    type=p.get("type", "string"),
                    description=p.get("description", ""),
                    required=p.get("required", True),
                    enum=p.get("enum"),
                    default=p.get("default"),
                )
                for p in parameters
            ]

            tool = MCPTool(
                name=name,
                description=description,
                parameters=params,
                handler=fn,
                category=category,
                require_auth=require_auth,
            )

            self._tools[name] = tool
            self._usage_stats[name] = 0
            logger.info(f"[MCP Registry] Registered tool: {name}")
            return fn

        return decorator

    # ── Lookup ────────────────────────────────────────────

    def get(self, name: str) -> Optional[MCPTool]:
        return self._tools.get(name)

    def list_all(self) -> list[MCPTool]:
        return [t for t in self._tools.values() if t.enabled]

    def list_by_category(self, category: str) -> list[MCPTool]:
        return [t for t in self._tools.values() if t.category == category and t.enabled]

    # ── Stats ─────────────────────────────────────────────

    def record_usage(self, name: str):
        if name in self._usage_stats:
            self._usage_stats[name] += 1

    def get_stats(self) -> dict:
        return {
            name: {"calls": count, "enabled": self._tools[name].enabled}
            for name, count in self._usage_stats.items()
        }

    # ── Enable / Disable ──────────────────────────────────

    def set_enabled(self, name: str, enabled: bool) -> bool:
        if name in self._tools:
            self._tools[name].enabled = enabled
            return True
        return False

    # ── Schema Export ─────────────────────────────────────

    def to_mcp_list(self) -> list[dict]:
        """Return all tools in MCP tools/list format."""
        return [tool.to_schema() for tool in self.list_all()]


# ── Singleton ──────────────────────────────────────────────
tool_registry = ToolRegistry()
