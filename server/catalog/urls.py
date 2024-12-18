from django.urls import path
from .views import (
CategoriesApiView
)

urlpatterns = [
    path('categories/', CategoriesApiView.as_view, name='categories'),
]