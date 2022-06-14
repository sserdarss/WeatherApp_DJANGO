from django.urls import path
from .views import delete, home

urlpatterns = [
 path('', home, name="home"),
 path('delete/<int:id>', delete, name="delete"),
]