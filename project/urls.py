from django.contrib import admin
from django.urls import path
from bg_tasks.views import send_task

urlpatterns = [
    path('admin/', admin.site.urls),
    path('send-task/', send_task, name='send_task'),
]
