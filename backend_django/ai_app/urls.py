# ai/urls.py
from django.urls import path
from .views import ChatStreamView, ModelsListView

urlpatterns = [
    path("chat/stream/", ChatStreamView.as_view()),  # 💬 streaming chat
    path("models/", ModelsListView.as_view()),  # 📦 models list
]
