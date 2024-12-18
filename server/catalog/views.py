from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from catalog.serilaizers import CategorySerializer

from catalog.models import Category


class CategoriesApiView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer