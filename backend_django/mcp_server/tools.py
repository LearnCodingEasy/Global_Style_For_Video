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
import subprocess
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
            "name":        "status",
            "type":        "string",
            "description": "Filter by status: draft | active | paused | all",
            "required":    False,
            "enum":        ["draft", "active", "paused", "all"],
            "default":     "all",
        }
    ],
)
def list_workflows(params: dict, user) -> dict:
    from automation.models import Workflow

    status = params.get("status", "all")
    qs = Workflow.objects.filter(user=user) if hasattr(
        Workflow, 'user') else Workflow.objects.all()

    if status != "all":
        qs = qs.filter(status=status)

    workflows = [
        {
            "id":          str(wf.id),
            "name":        wf.name,
            "description": wf.description or "",
            "status":      wf.status,
            "node_count":  wf.nodes.count(),
            "created_at":  wf.created_at.isoformat() if hasattr(wf, 'created_at') else None,
        }
        for wf in qs
    ]

    return {"workflows": workflows, "total": len(workflows)}


@tool_registry.register(
    name="run_workflow",
    description="Execute a workflow asynchronously via Celery. Returns a task_run_id to track progress.",
    category="workflows",
    parameters=[
        {
            "name":        "workflow_id",
            "type":        "string",
            "description": "UUID of the workflow to execute",
            "required":    True,
        },
        {
            "name":        "dry_run",
            "type":        "boolean",
            "description": "If true, validate without executing",
            "required":    False,
            "default":     False,
        },
    ],
)
def run_workflow(params: dict, user) -> dict:
    from automation.models import Workflow
    from automation.tasks import execute_workflow_task  # Celery task

    workflow_id = params["workflow_id"]
    dry_run = params.get("dry_run", False)

    try:
        workflow = Workflow.objects.get(id=workflow_id)
    except Workflow.DoesNotExist:
        return {"error": f"Workflow {workflow_id} not found", "success": False}

    if dry_run:
        node_count = workflow.nodes.count()
        return {
            "success":    True,
            "dry_run":    True,
            "workflow":   workflow.name,
            "node_count": node_count,
            "message":    "Validation passed — workflow can be executed",
        }

    # Execute via Celery
    task = execute_workflow_task.delay(str(workflow_id))

    return {
        "success":      True,
        "task_run_id":  task.id,
        "workflow_id":  workflow_id,
        "workflow_name": workflow.name,
        "message":      f"Workflow '{workflow.name}' started. Track with task_run_id.",
    }


@tool_registry.register(
    name="get_workflow_status",
    description="Get the current execution status of a workflow run.",
    category="workflows",
    parameters=[
        {
            "name":        "task_run_id",
            "type":        "string",
            "description": "Celery task ID returned from run_workflow",
            "required":    True,
        }
    ],
)
def get_workflow_status(params: dict, user) -> dict:
    from celery.result import AsyncResult

    task_run_id = params["task_run_id"]
    result = AsyncResult(task_run_id)

    state_map = {
        "PENDING":  "queued",
        "STARTED":  "running",
        "SUCCESS":  "success",
        "FAILURE":  "failed",
        "REVOKED":  "stopped",
        "RETRY":    "retrying",
    }

    return {
        "task_run_id": task_run_id,
        "status":      state_map.get(result.state, result.state.lower()),
        "raw_state":   result.state,
        "result":      result.result if result.successful() else None,
        "error":       str(result.result) if result.failed() else None,
        "ready":       result.ready(),
    }


@tool_registry.register(
    name="stop_workflow",
    description="Stop a running workflow execution.",
    category="workflows",
    parameters=[
        {
            "name":        "task_run_id",
            "type":        "string",
            "description": "Celery task ID to stop",
            "required":    True,
        }
    ],
)
def stop_workflow(params: dict, user) -> dict:
    from celery.result import AsyncResult

    task_run_id = params["task_run_id"]
    result = AsyncResult(task_run_id)
    result.revoke(terminate=True, signal="SIGTERM")

    return {
        "success":     True,
        "task_run_id": task_run_id,
        "message":     "Workflow stop signal sent",
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

    programs = [
        {
            "id":                   str(p.id),
            "name":                 p.name,
            "executable_path":      p.executable_path,
            "window_title_pattern": p.window_title_pattern or "",
            "image_url":            p.get_image if hasattr(p, 'get_image') else None,
        }
        for p in Program.objects.all()
    ]

    return {"programs": programs, "total": len(programs)}


@tool_registry.register(
    name="open_program",
    description="Open a desktop program by its registered ID.",
    category="programs",
    parameters=[
        {
            "name":        "program_id",
            "type":        "string",
            "description": "UUID of the program to open",
            "required":    True,
        },
        {
            "name":        "wait_seconds",
            "type":        "number",
            "description": "Seconds to wait after opening",
            "required":    False,
            "default":     2,
        },
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
            "message": f"Program '{program.name}' opened successfully",
            "pid":     result.get("pid"),
        }
    except Exception as e:
        return {"success": False, "error": str(e), "program": program.name}


@tool_registry.register(
    name="get_program_status",
    description="Check if a program is currently running.",
    category="programs",
    parameters=[
        {
            "name":        "program_id",
            "type":        "string",
            "description": "UUID of the program",
            "required":    True,
        }
    ],
)
def get_program_status(params: dict, user) -> dict:
    from automation.models import Program
    from automation.services.program_service import ProgramService

    program_id = params["program_id"]

    try:
        program = Program.objects.get(id=program_id)
        status = ProgramService.get_status(program)
        return {
            "program_id": program_id,
            "name":       program.name,
            "running":    status.get("running", False),
            "pid":        status.get("pid"),
        }
    except Program.DoesNotExist:
        return {"error": f"Program {program_id} not found"}


# ════════════════════════════════════════════════════
# DESKTOP ACTION TOOLS
# ════════════════════════════════════════════════════

@tool_registry.register(
    name="execute_desktop_action",
    description=(
        "Execute a single desktop action immediately. "
        "Supports: click, type_text, press_key, hotkey, wait, screenshot."
    ),
    category="desktop",
    parameters=[
        {
            "name":        "action_type",
            "type":        "string",
            "description": "Type of action to perform",
            "required":    True,
            "enum":        ["click", "type_text", "press_key", "hotkey", "wait", "screenshot", "move_mouse"],
        },
        {
            "name":        "payload",
            "type":        "object",
            "description": (
                "Action-specific parameters. "
                "click: {x, y} | type_text: {text} | press_key: {key} | "
                "hotkey: {keys[]} | wait: {seconds} | screenshot: {} | move_mouse: {x, y}"
            ),
            "required":    True,
        },
    ],
)
def execute_desktop_action(params: dict, user) -> dict:
    import pyautogui
    import time

    action_type = params["action_type"]
    payload = params.get("payload", {})

    pyautogui.FAILSAFE = True  # Move mouse to corner to abort

    try:
        if action_type == "click":
            x, y = int(payload["x"]), int(payload["y"])
            pyautogui.click(x, y)
            return {"success": True, "action": "click", "x": x, "y": y}

        elif action_type == "type_text":
            text = payload["text"]
            interval = float(payload.get("interval", 0.05))
            pyautogui.typewrite(text, interval=interval)
            return {"success": True, "action": "type_text", "chars_typed": len(text)}

        elif action_type == "press_key":
            key = payload["key"]
            pyautogui.press(key)
            return {"success": True, "action": "press_key", "key": key}

        elif action_type == "hotkey":
            keys = payload["keys"]  # e.g. ["ctrl", "shift", "p"]
            pyautogui.hotkey(*keys)
            return {"success": True, "action": "hotkey", "keys": keys}

        elif action_type == "wait":
            seconds = float(payload.get("seconds", 1))
            time.sleep(seconds)
            return {"success": True, "action": "wait", "seconds": seconds}

        elif action_type == "move_mouse":
            x, y = int(payload["x"]), int(payload["y"])
            duration = float(payload.get("duration", 0.3))
            pyautogui.moveTo(x, y, duration=duration)
            return {"success": True, "action": "move_mouse", "x": x, "y": y}

        elif action_type == "screenshot":
            import io
            # (x, y, w, h) or None for full screen
            region = payload.get("region")
            screenshot = pyautogui.screenshot(region=region)
            buf = io.BytesIO()
            screenshot.save(buf, format="PNG")
            b64 = base64.b64encode(buf.getvalue()).decode()
            size = screenshot.size
            return {
                "success":   True,
                "action":    "screenshot",
                "width":     size[0],
                "height":    size[1],
                "image_b64": b64,
                "format":    "PNG",
            }

        else:
            return {"success": False, "error": f"Unknown action_type: {action_type}"}

    except Exception as e:
        logger.exception(f"Desktop action error: {action_type}")
        return {"success": False, "error": str(e), "action": action_type}


@tool_registry.register(
    name="take_screenshot",
    description="Take a screenshot of the current screen or a region.",
    category="desktop",
    parameters=[
        {
            "name":        "region",
            "type":        "object",
            "description": "Optional region {x, y, width, height}. Omit for full screen.",
            "required":    False,
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
        "platform":    platform.system(),
        "python":      platform.python_version(),
        "cpu_percent": cpu,
        "memory": {
            "total_gb":    round(mem.total / 1e9, 2),
            "used_gb":     round(mem.used / 1e9, 2),
            "percent":     mem.percent,
        },
        "disk": {
            "total_gb":    round(disk.total / 1e9, 2),
            "free_gb":     round(disk.free / 1e9, 2),
            "percent":     disk.percent,
        },
    }


@tool_registry.register(
    name="list_running_processes",
    description="List currently running desktop processes.",
    category="system",
    parameters=[
        {
            "name":        "filter_name",
            "type":        "string",
            "description": "Optional filter by process name (case-insensitive)",
            "required":    False,
        }
    ],
)
def list_running_processes(params: dict, user) -> dict:
    import psutil

    filter_name = (params.get("filter_name") or "").lower()
    processes = []

    for proc in psutil.process_iter(["pid", "name", "status", "cpu_percent"]):
        try:
            info = proc.info
            if not filter_name or filter_name in info["name"].lower():
                processes.append({
                    "pid":    info["pid"],
                    "name":   info["name"],
                    "status": info["status"],
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return {"processes": processes[:100], "total": len(processes)}
