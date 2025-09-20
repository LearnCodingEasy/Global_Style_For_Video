## Django

### 1️⃣ Install

<div dir="rtl" style="font-size:1.5vw">
  
  هو إطار العمل اللي بيوفر لك الـ API نفسها، لكن مش مسؤول عن التحكم في السماح أو المنع بناءً على الدومين.
  
</div>

#### 1️⃣ Install 📚

<div dir="rtl" style="font-size:1.5vw">
  افتح الـ Terminal في مشروع Django واكتب:
</div>

```cmd
pip install djangorestframework
```

### 2️⃣ Setup 🛠️

<div dir="rtl" style="font-size:1.5vw">
</div>

```python
INSTALLED_APPS = [
  # Libraries
  'rest_framework',
]
```

### 3️⃣ used

<div dir="rtl" style="font-size:1.5vw">
  استخدام APIView (التحكم الكامل):
</div>

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

class PostListCreateView(APIView):
def get(self, request):
posts = Post.objects.all()
serializer = PostSerializer(posts, many=True)
return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

```

<div dir="rtl" style="font-size:1.5vw">
  استخدام ViewSets (الأفضل في المشاريع الكبيرة):
</div>

```python
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
queryset = Post.objects.all()
serializer_class = PostSerializer

```


