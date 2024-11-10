from django.db.models import Count
from rest_framework import filters


class ArticlesFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        param_value = request.query_params.get('comment')
        if param_value == 'comment':
            return queryset.annotate(comment_count=Count('comments')).order_by('comment_count')
        elif param_value == '-comment':
            return queryset.annotate(comment_count=Count('comments')).order_by('-comment_count')
        else:
            return queryset
