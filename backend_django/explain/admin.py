# backend_django\automation\admin.py


from django.contrib import admin

from .models import ExplainCategory
from .models import Explain


admin.site.register(ExplainCategory)
admin.site.register(Explain)
