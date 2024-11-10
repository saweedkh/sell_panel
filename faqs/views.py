# Local Apps
from .models import (
    Category as FAQCategory,
    FAQItems,
    TermsCategory,
    TermsItems
)
from .serializers import (
    FAQCategoryListSerializer,
    FAQListSerializer,
    TermsCategoryListSerializer,
    TermsItemsListSerializer,
)

# Third Party Packages
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny


class FAQCategoryListView(ListAPIView):
    """Get all faqs categories."""
    serializer_class = FAQCategoryListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return FAQCategory.objects.filter(display=True)


class FAQListView(ListAPIView):
    """Get all faqs."""
    permission_classes = (AllowAny,)
    serializer_class = FAQListSerializer
    filterset_fields = ('category',)

    def get_queryset(self):
        return FAQItems.objects.select_related('category').filter(display=True)


class TermsCategoryListView(ListAPIView):
    """Get all faqs categories."""
    serializer_class = TermsCategoryListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return TermsCategory.objects.filter(display=True)


class TermsItemsListView(ListAPIView):
    """Get all faqs."""
    permission_classes = (AllowAny,)
    serializer_class = TermsItemsListSerializer
    filterset_fields = ('category',)

    def get_queryset(self):
        return TermsItems.objects.select_related('category').filter(display=True)
