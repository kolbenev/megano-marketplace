from django.db.models import Count, Avg
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView

from catalog.models import Category
from product.models import Product, Sale
from catalog.filters import CatalogFilter
from catalog.serializers import CategorySerializer
from catalog.pagination import CustomPagination, SalePagination
from product.serializers import ProductShortSerializers, SaleSerializers


class CategoriesApiView(ListAPIView):
    """
    Эндпоинт для вывода всех Категорий.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CatalogListAPIView(ListAPIView):
    """
    Эндпоинт для получения списка продуктов с дополнительной
    информацией о количестве отзывов и среднем рейтинге каждого
    продукта. Поддерживает пагинацию, фильтрацию и сортировку.
    """

    queryset = Product.objects.annotate(
        reviews_count=Count("reviews"), rating=Avg("reviews__rate")
    )
    filterset_class = CatalogFilter
    serializer_class = ProductShortSerializers
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]


class ProductPopularAPIView(RetrieveAPIView):
    """
    Эндпоинт для вывода самого популярного товара.
    """

    serializer_class = ProductShortSerializers

    def get_object(self):
        return (
            Product.objects.annotate(
                reviews_count=Count("reviews"), average_rating=Avg("reviews__rate")
            )
            .order_by("-reviews_count")
            .first()
        )


class ProductLimitedAPIView(ListAPIView):
    """
    Эндпоинт для вывода товаров с остатком менее 10.
    """

    serializer_class = ProductShortSerializers

    def get_queryset(self):
        return Product.objects.filter(count__lt=10)


class SalesListAPIView(ListAPIView):
    """
    Эндпоинт для вывода всех товаров со скидкой.
    """

    queryset = Sale.objects.all()
    serializer_class = SaleSerializers
    pagination_class = SalePagination


class BannersListAPIView(ListAPIView):
    """
    Эндпоинт для вывода предметов баннера.
    """

    queryset = Product.objects.annotate(
        reviews_count=Count("reviews"), rating=Avg("reviews__rate")
    )
    serializer_class = ProductShortSerializers
