"""
mcp_server/tools.py

All MCP tools for the Automation Dashboard.
Each tool maps to a Django service.

Tools:
  Workflows:  list_workflows, run_workflow, get_workflow_status, stop_workflow
  Nodes:      list_workflow_nodes, run_single_node
  Programs:   list_programs, open_program, close_program, get_program_status
  Desktop:    execute_desktop_action, take_screenshot
  System:     get_system_info, list_running_processes
"""

from __future__ import annotations

import logging
import base64
from typing import Any

from .registry import tool_registry

logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════
# WORKFLOW TOOLS
# ════════════════════════════════════════════════════

@tool_registry.register(
    name="list_workflows",
    description="List all automation workflows with their status and metadata.",
    category="workflows",
    parameters=[
        {
            "name": "status",
            "type": "string",
            "description": "Filter by status: draft | active | paused | all",
            "required": False,
            "enum": ["draft", "active", "paused", "all"],
            "default": "all",
        }
    ],
)
def list_workflows(params: dict, user) -> dict:
    from automation.models import Workflow

    status = params.get("status", "all")

    qs = (
        Workflow.objects.filter(user=user)
        if hasattr(Workflow, "user")
        else Workflow.objects.all()
    )

    if status != "all":
        qs = qs.filter(status=status)

    workflows = [
        {
            "id": str(wf.id),
            "name": wf.name,
            "description": wf.description or "",
            "status": wf.status,
            "node_count": wf.nodes.count(),
            "created_at": wf.created_at.isoformat()
            if hasattr(wf, "created_at")
            else None,
        }
        for wf in qs
    ]

    return {"workflows": workflows, "total": len(workflows)}


@tool_registry.register(
    name="run_workflow",
    description="Execute a workflow asynchronously via Celery.",
    category="workflows",
    parameters=[
        {
            "name": "workflow_id",
            "type": "string",
            "description": "UUID of the workflow to execute",
            "required": True,
        },
        {
            "name": "dry_run",
            "type": "boolean",
            "description": "If true, validate without executing",
            "required": False,
            "default": False,
        },
    ],
)
def run_workflow(params: dict, user) -> dict:
    from automation.models import Workflow
    from automation.tasks import execute_workflow_task

    workflow_id = params["workflow_id"]
    dry_run = params.get("dry_run", False)

    try:
        workflow = Workflow.objects.get(id=workflow_id)
    except Workflow.DoesNotExist:
        return {"error": f"Workflow {workflow_id} not found", "success": False}

    if dry_run:
        return {
            "success": True,
            "dry_run": True,
            "workflow": workflow.name,
            "node_count": workflow.nodes.count(),
            "message": "Validation passed — workflow can be executed",
        }

    task = execute_workflow_task.delay(str(workflow_id))

    return {
        "success": True,
        "task_run_id": task.id,
        "workflow_id": workflow_id,
        "workflow_name": workflow.name,
        "message": f"Workflow '{workflow.name}' started.",
    }


@tool_registry.register(
    name="get_workflow_status",
    description="Get the current execution status of a workflow run.",
    category="workflows",
    parameters=[
        {
            "name": "task_run_id",
            "type": "string",
            "description": "Celery task ID",
            "required": True,
        }
    ],
)
def get_workflow_status(params: dict, user) -> dict:
    from celery.result import AsyncResult

    task_run_id = params["task_run_id"]
    result = AsyncResult(task_run_id)

    state_map = {
        "PENDING": "queued",
        "STARTED": "running",
        "SUCCESS": "success",
        "FAILURE": "failed",
        "REVOKED": "stopped",
        "RETRY": "retrying",
    }

    return {
        "task_run_id": task_run_id,
        "status": state_map.get(result.state, result.state.lower()),
        "raw_state": result.state,
        "result": result.result if result.successful() else None,
        "error": str(result.result) if result.failed() else None,
        "ready": result.ready(),
    }


@tool_registry.register(
    name="stop_workflow",
    description="Stop a running workflow execution.",
    category="workflows",
    parameters=[
        {
            "name": "task_run_id",
            "type": "string",
            "required": True,
        }
    ],
)
def stop_workflow(params: dict, user) -> dict:
    from celery.result import AsyncResult

    task_run_id = params["task_run_id"]
    result = AsyncResult(task_run_id)

    result.revoke(terminate=True, signal="SIGTERM")

    return {
        "success": True,
        "task_run_id": task_run_id,
        "message": "Workflow stop signal sent",
    }


# ════════════════════════════════════════════════════
# PROGRAM TOOLS
# ════════════════════════════════════════════════════

@tool_registry.register(
    name="list_programs",
    description="List all registered desktop programs.",
    category="programs",
    parameters=[],
    require_auth=True,
)
def list_programs(params: dict, user) -> dict:
    from automation.models import Program

    programs = []

    for p in Program.objects.all():
        image_url = None
        if hasattr(p, "get_image"):
            try:
                image_url = p.get_image()
            except Exception:
                image_url = None

        programs.append(
            {
                "id": str(p.id),
                "name": p.name,
                "executable_path": p.executable_path,
                "window_title_pattern": p.window_title_pattern or "",
                "image_url": image_url,
            }
        )

    return {"programs": programs, "total": len(programs)}


@tool_registry.register(
    name="open_program",
    description="Open a desktop program by its registered ID.",
    category="programs",
    parameters=[
        {"name": "program_id", "type": "string", "required": True},
        {"name": "wait_seconds", "type": "number", "required": False, "default": 2},
    ],
)
def open_program(params: dict, user) -> dict:
    from automation.models import Program
    from automation.services.program_service import ProgramService

    program_id = params["program_id"]
    wait_seconds = params.get("wait_seconds", 2)

    try:
        program = Program.objects.get(id=program_id)
    except Program.DoesNotExist:
        return {"error": f"Program {program_id} not found", "success": False}

    try:
        result = ProgramService.open(program, wait_seconds=wait_seconds)

        return {
            "success": True,
            "program": program.name,
            "pid": result.get("pid"),
        }

    except Exception as e:
        logger.exception("open_program failed")
        return {"success": False, "error": str(e)}


# ════════════════════════════════════════════════════
# DESKTOP ACTIONS
# ════════════════════════════════════════════════════

@tool_registry.register(
    name="execute_desktop_action",
    description="Execute a single desktop action immediately.",
    category="desktop",
    parameters=[
        {"name": "action_type", "type": "string", "required": True},
        {"name": "payload", "type": "object", "required": True},
    ],
)
def execute_desktop_action(params: dict, user) -> dict:
    import pyautogui
    import time
    import io

    action_type = params["action_type"]
    payload = params.get("payload", {})

    pyautogui.FAILSAFE = True

    try:
        if action_type == "click":
            x = int(payload.get("x", 0))
            y = int(payload.get("y", 0))
            pyautogui.click(x, y)

            return {"success": True, "action": "click", "x": x, "y": y}

        elif action_type == "type_text":
            text = payload.get("text", "")
            interval = float(payload.get("interval", 0.05))

            pyautogui.typewrite(text, interval=interval)

            return {
                "success": True,
                "action": "type_text",
                "chars_typed": len(text),
            }

        elif action_type == "press_key":
            key = payload.get("key")
            pyautogui.press(key)

            return {"success": True, "action": "press_key", "key": key}

        elif action_type == "hotkey":
            keys = payload.get("keys", [])
            pyautogui.hotkey(*keys)

            return {"success": True, "action": "hotkey", "keys": keys}

        elif action_type == "wait":
            seconds = float(payload.get("seconds", 1))
            time.sleep(seconds)

            return {"success": True, "action": "wait", "seconds": seconds}

        elif action_type == "move_mouse":
            x = int(payload.get("x", 0))
            y = int(payload.get("y", 0))
            duration = float(payload.get("duration", 0.3))

            pyautogui.moveTo(x, y, duration=duration)

            return {"success": True, "action": "move_mouse", "x": x, "y": y}

        elif action_type == "screenshot":
            region = payload.get("region")

            if region:
                region = (
                    region["x"],
                    region["y"],
                    region["width"],
                    region["height"],
                )

            screenshot = pyautogui.screenshot(region=region)

            buf = io.BytesIO()
            screenshot.save(buf, format="PNG")

            b64 = base64.b64encode(buf.getvalue()).decode()

            width, height = screenshot.size

            return {
                "success": True,
                "action": "screenshot",
                "width": width,
                "height": height,
                "image_b64": b64,
                "format": "PNG",
            }

        else:
            return {"success": False, "error": f"Unknown action_type: {action_type}"}

    except Exception as e:
        logger.exception("Desktop action error")
        return {"success": False, "error": str(e)}


@tool_registry.register(
    name="take_screenshot",
    description="Take a screenshot of the screen or a region.",
    category="desktop",
    parameters=[
        {
            "name": "region",
            "type": "object",
            "required": False,
        }
    ],
)
def take_screenshot(params: dict, user) -> dict:
    return execute_desktop_action(
        {"action_type": "screenshot", "payload": {
            "region": params.get("region")}},
        user,
    )


# ════════════════════════════════════════════════════
# SYSTEM TOOLS
# ════════════════════════════════════════════════════

@tool_registry.register(
    name="get_system_info",
    description="Get information about the automation server system.",
    category="system",
    parameters=[],
    require_auth=True,
)
def get_system_info(params: dict, user) -> dict:
    import platform
    import psutil

    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "platform": platform.system(),
        "python": platform.python_version(),
        "cpu_percent": cpu,
        "memory": {
            "total_gb": round(mem.total / 1e9, 2),
            "used_gb": round(mem.used / 1e9, 2),
            "percent": mem.percent,
        },
        "disk": {
            "total_gb": round(disk.total / 1e9, 2),
            "free_gb": round(disk.free / 1e9, 2),
            "percent": disk.percent,
        },
    }


@tool_registry.register(
    name="list_running_processes",
    description="List currently running processes.",
    category="system",
    parameters=[
        {
            "name": "filter_name",
            "type": "string",
            "required": False,
        }
    ],
)
def list_running_processes(params: dict, user) -> dict:
    import psutil

    filter_name = (params.get("filter_name") or "").lower().strip()
    processes = []

    for proc in psutil.process_iter(["pid", "name", "status"]):
        try:
            info = proc.info
            name = (info.get("name") or "").lower()

            if not filter_name or filter_name in name:
                processes.append(
                    {
                        "pid": info.get("pid"),
                        "name": info.get("name"),
                        "status": info.get("status"),
                    }
                )

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return {"processes": processes[:100], "total": len(processes)}
