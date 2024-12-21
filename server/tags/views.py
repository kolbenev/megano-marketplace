from rest_framework.generics import ListAPIView

from tags.models import Tag
from tags.serializers import TagSerializer


class TagsDetailsAPIView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
