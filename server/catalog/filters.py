import django_filters

from core.models import Tag


class CatalogFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    minPrice = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    maxPrice = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    freeDelivery = django_filters.BooleanFilter(
        field_name="free_delivery", lookup_expr="exact"
    )
    available = django_filters.BooleanFilter(method="filter_available")
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(), field_name="tags__name", to_field_name="name"
    )

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(count__gt=0)
        return queryset
