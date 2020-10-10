from django.contrib import admin
from .models import Shop, ShopUser
models = [Shop, ShopUser]
# Register your models here.
admin.site.register(models)
