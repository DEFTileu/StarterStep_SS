from django.contrib import admin
from .models import User

# Регистрация моделей в административной панели
admin.site.register(User)
