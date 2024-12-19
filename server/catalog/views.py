from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg

from product.models import Product, Sale
from product.serilaizers import ProductShortSerializers, SaleSerializers
from catalog.filters import CatalogFilter
from catalog.pagination import CustomPagination
from catalog.models import Category
from catalog.serilaizers import CategorySerializer


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
    pagination_class = CustomPagination


class BannersListAPIView(ListAPIView):
    """
    Эндпоинт для вывода предметов баннера.
    """
    queryset = Product.objects.all()
    serializer_class = ProductShortSerializers
