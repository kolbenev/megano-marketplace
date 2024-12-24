from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination


class SalePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": self.page.paginator.num_pages,
            }
        )


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_query_param = "currentPage"
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self, data) -> Response:
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": self.page.paginator.num_pages,
                "pageSize": self.page.paginator.per_page,
            }
        )

    def paginate_queryset(self, queryset, request, view=None):
        current_page = request.query_params.get(self.page_query_param, None)
        limit = request.query_params.get(self.page_size_query_param, None)

        try:
            if current_page is not None:
                current_page = int(current_page)
                if current_page <= 0:
                    raise ValidationError()

            if limit is not None:
                limit = int(limit)
                if limit <= 0 or limit > self.max_page_size:
                    raise ValidationError()
        except ValueError:
            raise ValidationError()

        sort_field = request.query_params.get("sort", None)
        sort_type = request.query_params.get("sortType", "dec")

        if sort_field:
            sort_prefix = "-" if sort_type == "dec" else ""
            queryset = queryset.order_by(f"{sort_prefix}{sort_field}")

        return super().paginate_queryset(queryset, request, view)
