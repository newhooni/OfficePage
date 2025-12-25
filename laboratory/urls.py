from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_note/', views.get_note, name='get_note'),
    path('save_note/', views.save_note, name='save_note'),
]
