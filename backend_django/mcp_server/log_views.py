"""
mcp_server/log_views.py
GET /api/mcp/logs/?limit=50&tool=&errors=1
"""
from django.http  import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators        import method_decorator


class MCPLogsView(View):

    @method_decorator(login_required)
    def get(self, request):
        from .models import MCPToolLog

        limit       = min(int(request.GET.get("limit", 50)), 200)
        tool        = request.GET.get("tool", "")
        only_errors = request.GET.get("errors") == "1"

        qs = MCPToolLog.objects.select_related("session").order_by("-started_at")
        if tool:        qs = qs.filter(tool_name=tool)
        if only_errors: qs = qs.filter(success=False)

        logs = []
        for log in qs[:limit]:
            logs.append({
                "id":          str(log.id),
                "tool_name":   log.tool_name,
                "agent":       log.session.agent_name if log.session else "—",
                "arguments":   log.arguments,
                "result":      log.result,
                "error":       log.error or None,
                "success":     log.success,
                "duration_ms": log.duration_ms,
                "started_at":  log.started_at.isoformat(),
            })

        return JsonResponse({"logs": logs, "total": qs.count()})