# Django Page Api

<div dir="rtl" style="font-size:1.2vw; padding: 1rem 0; font-weight: 900;">
  إنشاء العناصر المراية و طريقة العرض و الفلاتر
</div>

## Noremal

### All

<div style="font-size:1.2vw; padding: 2rem 0 0 0; font-weight: 900;">
</div>

```python
# views.py
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializer

# 🏷️ دالة لجلب جميع الفئات
# 🛠️ فقط GET تعريف هذه الدالة كواجهة برمجية تدعم طلبات
@api_view(["GET"])
# 🔓 عدم استخدام مصادقة
@authentication_classes([])
# 🔓 عدم استخدام تصاريح
@permission_classes([])
def product_list(request):
    # 📚 جلب كل الفئات
    products = Product.objects.all()
    # 🔄 serializer باستخدام  JSON تحويل البيانات إلى صيغة
    serializer = ProductSerializer(products, many=True)
    # 📤 JSON إعادة البيانات بصيغة
    # return Response(serializer.data)
    return JsonResponse(serializer.data, safe=False)
```

```python
# views.py
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class product_list(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

```

### Single

```python

```

```python
# 🧐 Django كائن يُستخدم لبناء استعلامات معقدة في
from django.db.models import Q

# 📚 دالة لجلب بيانات دورة معينة باستخدام المعرف (pk)
@api_view(["GET"])
def course_detail(request, pk):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    # 📦 جلب الدورة إذا كان منشؤها موجودًا ضمن معرفات المستخدمين
    # 🔍 البحث عن الدورة المحددة باستخدام شرط أن تكون منشأة بواسطة المستخدم أو أصدقائه.
    course = Course.objects.filter(Q(created_by_id__in=list(user_ids))).get(pk=pk)

    # 🎨 تحويل بيانات الدورة إلى JSON باستخدام الـ Serializer
    course_serializer = CourseDetailSerializer(course)
    course_data = course_serializer.data

    # 🔐 التحقق من إذا كان المستخدم مصرحًا له
    # 🔐 التحقق من إذا كان المستخدم قد سجل الدخول
    if request.user.is_authenticated:
        # ✅ إذا كان مصرحًا له، يتم استخدام بيانات الدورة كما هي
        course_data = course_serializer.data
    else:
        # 🚫 إذا لم يكن مصرحًا له، تكون بيانات الدورة فارغة
        course_data = {}

    # 📚 جلب جميع الدروس المرتبطة بالدورة
    lesson = course.lessons.all()
    # 🎨 تحويل بيانات الدروس إلى JSON باستخدام الـ Serializer
    lesson_serializer = LessonListSerializer(lesson, many=True)
    lesson_data = lesson_serializer.data

    # 📝 إرجاع بيانات الدورة والدروس في صيغة JSON
    return JsonResponse(
        {
            "course": course_data,  # 📝 بيانات الدورة
            "lessons": lesson_data,  # 📚 بيانات الدروس
        }
    )

```

## viewsets

##### rest_framework viewsets

### All

```python
# Get All Data List By viewsets
from rest_framework import viewsets
from .models import Vendor
from .serializers import VendorSerializer

class vendorViews(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
```

### Single

#### Single By User By viewsets

```python
# Get All Data Created By User By viewsets
from rest_framework import viewsets
from .models import Vendor
from .serializers import VendorSerializer

class vendorViews(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
```

### Create

#### Create Data By viewsets

```python
# Create Data By viewsets
from rest_framework import viewsets
from .models import Vendor
from .serializers import VendorSerializer

class vendorViews(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
```

```python

```
