# ai_app/tasks.py
from django.views import View
from django.http import JsonResponse
from celery import shared_task
from django.core.cache import cache
from .services import OllamaService, ChatMessage


@shared_task(bind=True, max_retries=3)
def run_ai_task(self, task_id: str, prompt: str, model: str = "gemma3:4b"):
    """
    مثال: تحليل workflow automation بالذكاء الاصطناعي
    النتيجة بتتخزن في Redis Cache
    """
    try:
        service = OllamaService(model=model)
        messages = [
            ChatMessage(role="system",
                        content="أنت مساعد متخصص في أتمتة المهام"),
            ChatMessage(role="user", content=prompt),
        ]
        result = service.chat_sync(messages)

        # خزّن النتيجة في cache لمدة ساعة
        cache.set(f"ai_task_{task_id}", {
            "status": "done",
            "result": result,
        }, timeout=3600)

        return result
    except Exception as exc:
        cache.set(f"ai_task_{task_id}", {
                  "status": "error", "error": str(exc)}, timeout=600)
        raise self.retry(exc=exc, countdown=10)


# View للـ task status


class AITaskView(View):
    def post(self, request):
        import json
        import uuid
        body = json.loads(request.body)
        task_id = str(uuid.uuid4())
        run_ai_task.delay(task_id, body["prompt"],
                          body.get("model", "gemma3:4b"))
        return JsonResponse({"task_id": task_id, "status": "queued"})

    def get(self, request, task_id):
        result = cache.get(f"ai_task_{task_id}")
        if not result:
            return JsonResponse({"status": "pending"})
        return JsonResponse(result)
