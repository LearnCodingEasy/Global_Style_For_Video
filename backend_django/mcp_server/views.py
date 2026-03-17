"""
mcp_server/views.py

MCP HTTP Endpoint
POST /api/mcp/

Implements JSON-RPC 2.0 over HTTP.
Each request body = one MCPRequest.
Each response body = one MCPResponse.

Authentication:
  Bearer token in Authorization header.
  Token maps to MCPSession (tracks agent, usage, logs).

Rate Limiting:
  Per-session, configurable via settings.MCP_RATE_LIMIT_PER_MINUTE
"""

from __future__ import annotations
import json
import uuid
import logging
import time
from datetime import datetime, timedelta
from functools import wraps

from django.http         import JsonResponse
from django.views        import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators      import method_decorator
from django.conf                  import settings
from django.core.cache            import cache
from django.utils                 import timezone

from .protocol  import MCPRequest, MCPResponse, MCPError
from .registry  import tool_registry
from .models    import MCPSession, MCPToolLog

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────
MCP_VERSION       = "2024-11-05"
SERVER_NAME       = "automation-dashboard"
SERVER_VERSION    = "1.0.0"
RATE_LIMIT_RPM    = getattr(settings, "MCP_RATE_LIMIT_PER_MINUTE", 60)


# ══════════════════════════════════════════════════════════
# Authentication Helper
# ══════════════════════════════════════════════════════════

def get_session_from_request(request) -> MCPSession | None:
    """Extract and validate Bearer token → MCPSession."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None

    token = auth[7:].strip()
    try:
        session = MCPSession.objects.select_related("user").get(
            token     = token,
            is_active = True,
        )
        # Check expiry
        if session.expires_at and session.expires_at < timezone.now():
            session.is_active = False
            session.save(update_fields=["is_active"])
            return None
        return session
    except MCPSession.DoesNotExist:
        return None


def check_rate_limit(session: MCPSession) -> bool:
    """Redis/cache-based rate limiting per session."""
    key   = f"mcp:ratelimit:{session.id}"
    count = cache.get(key, 0)

    if count >= RATE_LIMIT_RPM:
        return False

    cache.set(key, count + 1, timeout=60)
    return True


# ══════════════════════════════════════════════════════════
# MCP Method Handlers
# ══════════════════════════════════════════════════════════

def handle_initialize(request_obj: MCPRequest, session: MCPSession) -> dict:
    """MCP initialize — return server capabilities."""
    # Update session with client info
    client_info = request_obj.params.get("clientInfo", {})
    if client_info:
        session.agent_name    = client_info.get("name", session.agent_name)
        session.agent_version = client_info.get("version", "")
        session.last_seen     = timezone.now()
        session.save(update_fields=["agent_name", "agent_version", "last_seen"])

    return {
        "protocolVersion": MCP_VERSION,
        "serverInfo": {
            "name":    SERVER_NAME,
            "version": SERVER_VERSION,
        },
        "capabilities": {
            "tools":     {"listChanged": True},
            "resources": {"subscribe": False, "listChanged": False},
            "prompts":   {"listChanged": False},
            "logging":   {},
        },
        "instructions": (
            "Automation Dashboard MCP Server. "
            "Use tools to control desktop workflows, run programs, "
            "and execute automation sequences."
        ),
    }


def handle_tools_list(request_obj: MCPRequest, session: MCPSession) -> dict:
    """Return all enabled tools."""
    return {"tools": tool_registry.to_mcp_list()}


def handle_tools_call(request_obj: MCPRequest, session: MCPSession) -> dict:
    """Execute a tool and return result."""
    params    = request_obj.params or {}
    tool_name = params.get("name", "")
    arguments = params.get("arguments", {})

    tool = tool_registry.get(tool_name)

    if tool is None:
        raise ToolNotFoundError(tool_name)

    if not tool.enabled:
        raise ToolDisabledError(tool_name)

    # Log the call
    log_entry = MCPToolLog.objects.create(
        session    = session,
        tool_name  = tool_name,
        arguments  = arguments,
        started_at = timezone.now(),
    )

    start_time = time.monotonic()

    try:
        result = tool.handler(arguments, session.user)
        duration_ms = int((time.monotonic() - start_time) * 1000)

        # Update log
        log_entry.result       = result
        log_entry.success      = True
        log_entry.duration_ms  = duration_ms
        log_entry.completed_at = timezone.now()
        log_entry.save()

        tool_registry.record_usage(tool_name)

        # MCP tools/call response format
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, ensure_ascii=False, indent=2),
                }
            ],
            "isError": False,
        }

    except Exception as e:
        duration_ms = int((time.monotonic() - start_time) * 1000)
        error_msg   = str(e)

        log_entry.error        = error_msg
        log_entry.success      = False
        log_entry.duration_ms  = duration_ms
        log_entry.completed_at = timezone.now()
        log_entry.save()

        logger.exception(f"Tool execution error: {tool_name}")

        return {
            "content": [{"type": "text", "text": f"Tool error: {error_msg}"}],
            "isError": True,
        }


def handle_resources_list(request_obj: MCPRequest, session: MCPSession) -> dict:
    """List available resources (workflow definitions as documents)."""
    from automation.models import Workflow

    resources = []
    for wf in Workflow.objects.all()[:50]:
        resources.append({
            "uri":      f"automation://workflow/{wf.id}",
            "name":     wf.name,
            "mimeType": "application/json",
            "description": wf.description or f"Workflow: {wf.name}",
        })

    return {"resources": resources}


def handle_prompts_list(request_obj: MCPRequest, session: MCPSession) -> dict:
    """Built-in prompt templates for common automation tasks."""
    return {
        "prompts": [
            {
                "name":        "automate_task",
                "description": "Generate an automation workflow for a described task",
                "arguments": [
                    {"name": "task_description", "description": "What to automate", "required": True},
                    {"name": "target_program",   "description": "Target application", "required": False},
                ],
            },
            {
                "name":        "debug_workflow",
                "description": "Analyze and debug a failing workflow",
                "arguments": [
                    {"name": "workflow_id",  "description": "Workflow UUID", "required": True},
                    {"name": "error_log",    "description": "Error message",  "required": False},
                ],
            },
        ]
    }


# ── Routing Table ─────────────────────────────────────────
METHOD_HANDLERS = {
    "initialize":      handle_initialize,
    "tools/list":      handle_tools_list,
    "tools/call":      handle_tools_call,
    "resources/list":  handle_resources_list,
    "prompts/list":    handle_prompts_list,
}


# ══════════════════════════════════════════════════════════
# Custom Exceptions
# ══════════════════════════════════════════════════════════

class ToolNotFoundError(Exception):
    def __init__(self, name): self.name = name

class ToolDisabledError(Exception):
    def __init__(self, name): self.name = name


# ══════════════════════════════════════════════════════════
# Main MCP View
# ══════════════════════════════════════════════════════════

@method_decorator(csrf_exempt, name="dispatch")
class MCPView(View):
    """
    POST /api/mcp/
    Handles all MCP JSON-RPC requests.
    """

    def post(self, request):
        # ── Parse body ────────────────────────────────────
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return self._json_error(None, MCPError.PARSE_ERROR, "Invalid JSON")

        req = MCPRequest.from_dict(body)

        # ── Authenticate ──────────────────────────────────
        # initialize doesn't require auth — creates session
        if req.method == "initialize":
            session = self._get_or_create_session(request)
        else:
            session = get_session_from_request(request)
            if session is None:
                return self._json_error(
                    req.id, MCPError.AUTH_REQUIRED,
                    "Valid Bearer token required",
                )

        # ── Rate limit ────────────────────────────────────
        if not check_rate_limit(session):
            return self._json_error(
                req.id, MCPError.RATE_LIMITED,
                f"Rate limit exceeded: {RATE_LIMIT_RPM} requests/minute",
            )

        # ── Update last_seen ──────────────────────────────
        session.last_seen = timezone.now()
        session.request_count = (session.request_count or 0) + 1
        session.save(update_fields=["last_seen", "request_count"])

        # ── Route to handler ──────────────────────────────
        handler = METHOD_HANDLERS.get(req.method)

        if handler is None:
            return self._json_error(
                req.id, MCPError.METHOD_NOT_FOUND,
                f"Method not found: {req.method}",
            )

        try:
            result   = handler(req, session)
            response = MCPResponse.success(req.id, result)
        except ToolNotFoundError as e:
            response = MCPResponse.error(req.id, MCPError.TOOL_NOT_FOUND, f"Tool not found: {e.name}")
        except ToolDisabledError as e:
            response = MCPResponse.error(req.id, MCPError.TOOL_NOT_FOUND, f"Tool disabled: {e.name}")
        except Exception as e:
            logger.exception(f"MCP handler error for method: {req.method}")
            response = MCPResponse.error(req.id, MCPError.INTERNAL_ERROR, str(e))

        return JsonResponse(response.to_dict())

    def _json_error(self, id, code, message):
        resp = MCPResponse.error(id, code, message)
        return JsonResponse(resp.to_dict(), status=200)  # MCP always 200

    def _get_or_create_session(self, request) -> "MCPSession":
        """Create a new session on initialize."""
        import secrets
        token = secrets.token_urlsafe(32)

        session = MCPSession.objects.create(
            token      = token,
            is_active  = True,
            expires_at = timezone.now() + timedelta(days=7),
            ip_address = self._get_client_ip(request),
        )
        return session

    def _get_client_ip(self, request) -> str:
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")


# ══════════════════════════════════════════════════════════
# Session Management Views (REST — not MCP)
# ══════════════════════════════════════════════════════════

from django.contrib.auth.decorators import login_required
from django.utils.decorators        import method_decorator as deco


@method_decorator([csrf_exempt, login_required], name="dispatch")
class MCPTokenView(View):
    """
    POST /api/mcp/token/    → Create new token
    DELETE /api/mcp/token/  → Revoke token
    GET /api/mcp/sessions/  → List active sessions
    """

    def post(self, request):
        """Generate a new MCP token for the authenticated user."""
        import secrets
        from django.utils import timezone

        body  = json.loads(request.body or "{}")
        name  = body.get("name", "API Token")
        days  = int(body.get("expires_days", 30))

        session = MCPSession.objects.create(
            user       = request.user,
            token      = secrets.token_urlsafe(32),
            agent_name = name,
            is_active  = True,
            expires_at = timezone.now() + timedelta(days=days),
        )

        return JsonResponse({
            "token":      session.token,
            "session_id": str(session.id),
            "expires_at": session.expires_at.isoformat(),
            "message":    "Store this token securely — it won't be shown again.",
        })

    def delete(self, request):
        """Revoke a token."""
        body  = json.loads(request.body or "{}")
        token = body.get("token")

        revoked = MCPSession.objects.filter(
            user      = request.user,
            token     = token,
            is_active = True,
        ).update(is_active=False)

        return JsonResponse({"revoked": revoked > 0})


class MCPSessionsView(View):
    """GET /api/mcp/sessions/ — Dashboard: list all sessions + stats."""

    @method_decorator(login_required)
    def get(self, request):
        sessions = MCPSession.objects.filter(
            is_active=True
        ).order_by("-last_seen")[:50]

        data = []
        for s in sessions:
            data.append({
                "id":            str(s.id),
                "agent_name":    s.agent_name or "Unknown Agent",
                "agent_version": s.agent_version or "",
                "ip_address":    s.ip_address or "",
                "last_seen":     s.last_seen.isoformat() if s.last_seen else None,
                "request_count": s.request_count or 0,
                "expires_at":    s.expires_at.isoformat() if s.expires_at else None,
                "created_at":    s.created_at.isoformat() if hasattr(s, 'created_at') else None,
            })

        # Tool usage stats
        stats = tool_registry.get_stats()

        return JsonResponse({
            "sessions": data,
            "tool_stats": stats,
            "total_active": len(data),
        })


class MCPToolsView(View):
    """
    GET  /api/mcp/tools/           → List tools + enable state
    POST /api/mcp/tools/{name}/    → Toggle enable/disable
    """

    @method_decorator(login_required)
    def get(self, request):
        tools = []
        for tool in tool_registry.list_all():
            tools.append({
                "name":        tool.name,
                "description": tool.description,
                "category":    tool.category,
                "enabled":     tool.enabled,
                "require_auth": tool.require_auth,
                "schema":      tool.to_schema(),
            })

        return JsonResponse({"tools": tools})

    @method_decorator([csrf_exempt, login_required], name="dispatch")
    def post(self, request, tool_name):
        body    = json.loads(request.body or "{}")
        enabled = bool(body.get("enabled", True))

        success = tool_registry.set_enabled(tool_name, enabled)

        if not success:
            return JsonResponse({"error": f"Tool not found: {tool_name}"}, status=404)

        return JsonResponse({"tool": tool_name, "enabled": enabled})