from django.urls import path

from tags.views import TagsDetailsAPIView


urlpatterns = [
    path("tags/", TagsDetailsAPIView.as_view(), name="tags"),
]
