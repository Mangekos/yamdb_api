from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title,
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer,
                    
        
class CreateDestroyListViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
):
    pass


class CategoryGenreViewSet(CreateDestroyListViewSet):
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    ordering_fields = ('name',)
