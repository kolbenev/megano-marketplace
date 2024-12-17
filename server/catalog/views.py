from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from catalog.models import Category
from catalog.serializers import CategorySerializer


class CategoryListView(APIView):
    def get(self, request: Request) -> Response:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CatalogListView(APIView)
