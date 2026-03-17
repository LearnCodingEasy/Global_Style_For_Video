from django.contrib import admin
from .models import MCPSession, MCPToolLog


@admin.register(MCPSession)
class SessionAdmin(admin.ModelAdmin):

    list_display = (
        "agent_name",
        "user",
        "ip_address",
        "request_count",
        "last_seen",
        "is_active",
    )


@admin.register(MCPToolLog)
class ToolLogAdmin(admin.ModelAdmin):

    list_display = (
        "tool_name",
        "session",
        "success",
        "duration_ms",
        "started_at",
    )

    search_fields = ("tool_name",)
