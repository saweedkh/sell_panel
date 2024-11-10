# Django Built-in modules
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import gettext_lazy as _

# Locals apps
# from .models import AbstractBlogCategory, AbstractBlogPost
# from .serializers import (
#     CategoryListSerializer,
#     CategoryDetailSerializer,
#     PostListSerializer,
#     PostDetailSerializer,
# )
from .utils import make_automatic_description

# Third Party Packages
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny


# class CategoryListView(ListAPIView):
#     serializer_class = CategoryListSerializer
#     permission_classes = (AllowAny,)
#
#     def get_queryset(self):
#         return AbstractBlogCategory.objects.published()
#
#
# class CategoryDetailView(RetrieveAPIView):
#     lookup_field = 'slug'
#     serializer_class = CategoryDetailSerializer
#     permission_classes = (AllowAny,)
#
#     def get_queryset(self):
#         return AbstractBlogCategory.objects.published()


# class PostListView(ListAPIView):
#     serializer_class = PostListSerializer
#     permission_classes = (AllowAny,)
#     filterset_fields = ('category',)
#
#     def get_queryset(self):
#         return AbstractBlogPost.objects.published()
#
#
# class PostDetailView(RetrieveAPIView):
#     lookup_field = 'slug'
#     serializer_class = PostDetailSerializer
#     permission_classes = (AllowAny,)
#
#     def get_queryset(self):
#         return AbstractBlogPost.objects.published()


@login_required
@staff_member_required
def automate_description(request):
    try:
        content = request.POST['content']
        description = make_automatic_description(content)
        return JsonResponse({'status': 200, 'description': description, })
    except Exception as exception:
        return JsonResponse({'status': 500, 'message': _('مشکلی در ساخت خودکار توضیحات وجود دارد')})
