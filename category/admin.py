from django.contrib import admin
from .models import Category2, Category1, Category3
models = [Category2, Category1, Category3]
# Register your models here.

admin.site.register(models)
