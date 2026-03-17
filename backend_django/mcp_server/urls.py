# """
# mcp_server/urls.py
# """
# from django.urls import path
# from .views import MCPView, MCPTokenView, MCPSessionsView, MCPToolsView

# app_name = "mcp_server"

# urlpatterns = [
#     # Main MCP JSON-RPC endpoint
#     path("",             MCPView.as_view(),        name="mcp"),

#     # Session / token management
#     path("token/",       MCPTokenView.as_view(),   name="token"),
#     path("sessions/",    MCPSessionsView.as_view(), name="sessions"),

#     # Tool management
#     path("tools/",       MCPToolsView.as_view(),   name="tools_list"),
#     path("tools/<str:tool_name>/", MCPToolsView.as_view(), name="tool_toggle"),
# ]
from django.urls import path
from .views import (
    MCPView,
    MCPTokenView,
    MCPSessionsView,
    MCPToolsView
)
from .log_views import MCPLogsView

urlpatterns = [

    # MCP protocol endpoint
    path("/", MCPView.as_view()),

    # Token management
    path("token/", MCPTokenView.as_view()),

    # Dashboard endpoints
    path("sessions/", MCPSessionsView.as_view()),
    path("tools/", MCPToolsView.as_view()),
    path("tools/<str:tool_name>/", MCPToolsView.as_view()),
    path("logs/", MCPLogsView.as_view()),

]
