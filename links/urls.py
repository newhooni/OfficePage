from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_work/', views.get_work, name='get_work'),
    path('save_work/', views.save_work, name='save_work'),
]