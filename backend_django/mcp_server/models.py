"""
mcp_server/models.py

Database models for MCP Server:
  MCPSession  — tracks connected agents + tokens
  MCPToolLog  — audit log of every tool call
"""

import uuid
from django.db   import models
from django.conf import settings


class MCPSession(models.Model):
    """
    Represents one MCP agent connection.
    A session has a Bearer token and tracks usage.
    """
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user          = models.ForeignKey(
                        settings.AUTH_USER_MODEL,
                        null=True, blank=True,
                        on_delete=models.SET_NULL,
                        related_name="mcp_sessions",
                    )
    token         = models.CharField(max_length=128, unique=True, db_index=True)

    # Agent metadata (set during initialize)
    agent_name    = models.CharField(max_length=255, blank=True, default="")
    agent_version = models.CharField(max_length=64,  blank=True, default="")
    ip_address    = models.GenericIPAddressField(null=True, blank=True)

    # State
    is_active     = models.BooleanField(default=True, db_index=True)
    expires_at    = models.DateTimeField(null=True, blank=True)
    last_seen     = models.DateTimeField(null=True, blank=True)
    request_count = models.PositiveIntegerField(default=0)

    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table   = "mcp_sessions"
        ordering   = ["-last_seen"]
        verbose_name        = "MCP Session"
        verbose_name_plural = "MCP Sessions"

    def __str__(self):
        return f"{self.agent_name or 'Agent'} — {self.token[:12]}..."

    @property
    def is_expired(self):
        from django.utils import timezone
        return self.expires_at and self.expires_at < timezone.now()


class MCPToolLog(models.Model):
    """
    Immutable audit log for every tools/call invocation.
    """
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session     = models.ForeignKey(
                      MCPSession,
                      on_delete=models.CASCADE,
                      related_name="tool_logs",
                  )
    tool_name   = models.CharField(max_length=128, db_index=True)
    arguments   = models.JSONField(default=dict)
    result      = models.JSONField(null=True, blank=True)
    error       = models.TextField(blank=True, default="")
    success     = models.BooleanField(default=False, db_index=True)
    duration_ms = models.PositiveIntegerField(null=True)

    started_at   = models.DateTimeField(db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "mcp_tool_logs"
        ordering = ["-started_at"]
        verbose_name        = "MCP Tool Log"
        verbose_name_plural = "MCP Tool Logs"
        indexes = [
            models.Index(fields=["tool_name", "started_at"]),
            models.Index(fields=["session",   "started_at"]),
        ]

    def __str__(self):
        status = "✅" if self.success else "❌"
        return f"{status} {self.tool_name} ({self.duration_ms}ms)"