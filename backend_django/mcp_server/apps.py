

"""
mcp_server/apps.py
"""
from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class McpServerConfig(AppConfig):
    name           = "mcp_server"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name   = "MCP Server"

    def ready(self):
        """
        Import tools.py when Django starts.
        This triggers all @tool_registry.register() decorators,
        populating the ToolRegistry singleton.
        """
        try:
            import mcp_server.tools  # noqa: F401
            logger.info("[MCP] Tool registry loaded successfully")
        except Exception as e:
            logger.error(f"[MCP] Failed to load tools: {e}")