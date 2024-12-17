import django_filters
from product.models import Product

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    free_delivery = django_filters.BooleanFilter(field_name="free_delivery")
    available = django_filters.BooleanFilter(method='filter_available')

    class Meta:
        model = Product
        fields = ['name', 'min_price', 'max_price', 'free_delivery', 'available', 'category']

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(count__gt=0)
        return queryset
