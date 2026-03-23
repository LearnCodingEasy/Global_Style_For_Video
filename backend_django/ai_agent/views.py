# 📄 [ mcp_server/views.py ]
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .services import AIAgent
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status


class MCPView(APIView):
    # 1. تحديد طريقة التحقق من الهوية (JWT فقط لمنع الـ Redirects)
    authentication_classes = [JWTAuthentication]
    # 2. حماية المسار بحيث لا يدخله إلا مستخدم مسجل
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # استلام البيانات من الـ AIAgent
        data = request.data
        method = data.get("method")

        # مثال بسيط لمعالجة طلب tools/list
        if method == "tools/list":
            return Response({
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "result": {
                    "tools": [
                        {
                            "name": "example_tool",
                            "description": "A sample automation tool",
                            "input_schema": {
                                "type": "object",
                                "properties": {}
                            }
                        }
                    ]
                }
            })

        # إذا لم يتم التعرف على الـ Method
        return Response({
            "jsonrpc": "2.0",
            "id": data.get("id"),
            "error": {"code": -32601, "message": "Method not found"}
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class ExecutePromptView(View):

    def post(self, request):

        body = json.loads(request.body)

        prompt = body.get("prompt")
        token = body.get("token")

        results = AIAgent.execute_prompt(prompt, token)

        return JsonResponse({
            "prompt": prompt,
            "results": results
        })
