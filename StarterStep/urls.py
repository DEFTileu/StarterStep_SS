from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Панель администратора
    path('reg/', include('reg_auth.urls')),
    path('profile/',include('Profilee.urls')),
    path('', include('main.urls')),  
    # Главная страница и связанные маршруты
]
