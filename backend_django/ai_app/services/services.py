# ai_app/services/services.py

import requests
import json
from pydantic import BaseModel
from typing import Iterator

# 🖥️ السيرفر المحلي
OLLAMA_URL = "http://localhost:11434"


class ChatMessage(BaseModel):
    role: str  # 👤 user / system / assistant
    content: str  # 💬 النص


class OllamaService:
    def __init__(self, model: str = "phi"):
        self.model = model

    def chat_stream(self, messages):
        payload = {
            "model": self.model,  # 🤖 الموديل
            "messages": [m.model_dump() for m in messages],  # 📦 تحويل
            "stream": True,  # ⚡ streaming
        }

        with requests.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload,
            stream=True,  # 📡 مهم جدًا
            timeout=120
        ) as resp:

            for line in resp.iter_lines():  # 📥 قراءة chunk
                if line:
                    try:
                        chunk = json.loads(line)

                        # 🧠 استخراج النص
                        if 'message' in chunk and 'content' in chunk['message']:
                            yield chunk["message"]["content"]  # ✨ token

                        if chunk.get("done"):
                            break  # ✅ انتهى

                    except json.JSONDecodeError:
                        continue
    def chat_sync(self, messages):
        payload = {
            "model": self.model,
            "messages": [m.model_dump() for m in messages],
            "stream": False,  # ⛔ بدون streaming
        }

        resp = requests.post(f"{OLLAMA_URL}/api/chat", json=payload)
        return resp.json()["message"]["content"]  # 💬 الرد الكامل

    def list_models(self) -> list[str]:
        resp = requests.get(f"{OLLAMA_URL}/api/tags")
        return [m["name"] for m in resp.json().get("models", [])]
