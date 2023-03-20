from django_filters import FilterSet
from django_filters import CharFilter
from django_filters.rest_framework import filters
from novels.models import NovelModel

class NovelFilter(FilterSet):
    author = CharFilter(field_name='author__authorName',lookup_expr='contains', label='Author')
    genre = CharFilter(field_name='genre__name',lookup_expr='contains', label= 'genre')
    chapter = CharFilter(field_name='books__title', lookup_expr='contains', label='chapter')
    class Meta:
        model = NovelModel
        fields =  ['title', 'author', 'genre', 'chapter']