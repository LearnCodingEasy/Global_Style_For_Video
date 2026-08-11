# ai_app/views.py
import json  # 🔄 للتعامل مع JSON (request & response)
from django.http import StreamingHttpResponse, JsonResponse  # 📡 responses
from django.views import View  # 🧱 base class للـ views
from django.views.decorators.csrf import csrf_exempt  # 🔓 تعطيل CSRF (API)
from django.utils.decorators import method_decorator  # 🧩 لتطبيق decorator على class
from .services.services import OllamaService, ChatMessage  # 🧠 خدمة AI

"""
🧠 الفكرة هنا ببساطة:
المستخدم يبعت رسالة
Django يبعتها لـ Ollama
Ollama يرد token token
Django يرجّعها مباشرة للـ Vue

👉 كأنك بتعمل ChatGPT محلي 🔥

"""


@method_decorator(csrf_exempt, name='dispatch')  # 🚫 إلغاء CSRF
class ChatStreamView(View):

    def post(self, request):
        try:
            body = json.loads(request.body)  # 📥 تحويل request JSON → dict
        except json.JSONDecodeError:
            # ❌ JSON غلط
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # 🧠 تحويل الرسائل لـ Objects
        messages = [ChatMessage(**m) for m in body.get("messages", [])]

        model = body.get("model", "phi")  # 🤖 اختيار الموديل
        service = OllamaService(model=model)  # 🔌 إنشاء service

        # 🔥 دي أهم حتة (Streaming Generator)
        def event_stream():
            try:
                for token in service.chat_stream(messages):  # 📡 استلام حرف حرف
                    yield f"data: {json.dumps({'token': token}, ensure_ascii=False)}\n\n"
                    # ↑ بيرجع token للـ frontend

                yield "data: [DONE]\n\n"  # ✅ نهاية الرد
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"  # ❌ error

        # 📡 Response Streaming (زي ChatGPT)
        response = StreamingHttpResponse(
            streaming_content=event_stream(),
            content_type="text/event-stream; charset=utf-8",  # ⚡ SSE
        )

        response['Cache-Control'] = 'no-cache, no-transform'  # 🚫 كاش
        # 🚀 يمنع buffering (مهم للـ streaming)
        response['X-Accel-Buffering'] = 'no'

        return response

    # 🌐 دعم CORS Preflight
    def options(self, request, *args, **kwargs):
        response = JsonResponse({})
        response['Allow'] = 'POST, OPTIONS'
        return response


"""
💡 دي عشان:
تعرض phi / gemma في UI
"""


class ModelsListView(View):
    def get(self, request):
        service = OllamaService()  # 🧠 AI service
        # 📋 قائمة الموديلات
        return JsonResponse({"models": service.list_models()})
