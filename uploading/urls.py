from django.urls import path

from . import views

app_name = "uploading"

urlpatterns = [
    path('', views.index, name='index'),
]