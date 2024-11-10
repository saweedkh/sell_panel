# Django Build-in
from datetime import datetime, timezone

# Third Party Packages
# from captcha.helpers import captcha_image_url
# from captcha.models import CaptchaStore
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView, Response

# Local Apps
from .serializers import CategoryDetailSerializers, CategoryListSerializers
from utils.captcha_verify import get_captcha, verify
from .filters import ArticlesFilter
from .models import ArticlePost, ArticleComments, ArticleCommentsLikes, ArticleTag, Category
from .serializers import (
    ArticlePostSerializers,
    ArticlePostDetailSerializers,
    ArticleCommentLikesSerializers,
    ArticleCreateCommentsSerializers, ArticleTagSerializers
)


class CategoryListView(ListAPIView):
    """Get all articles categories."""
    serializer_class = CategoryListSerializers
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Category.objects.published().order_by('name')


class CategoryDetailView(RetrieveAPIView):
    """Get article category detail."""

    lookup_field = 'id'
    serializer_class = CategoryDetailSerializers
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Category.objects.published()


class ArticlePostListView(ListAPIView):
    """Get all post articles."""
    permission_classes = (AllowAny,)
    serializer_class = ArticlePostSerializers
    filter_backends = [ArticlesFilter, DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ('category__id', 'tag', 'is_important', 'article_type')
    ordering_fields = ('views', 'created')
    search_fields = ('name',)

    def get_queryset(self):
        if self.request.GET.get('show_in_head'):
            posts = self.request.GET.get('show_in_head')
            if posts == 'true':
                return ArticlePost.objects.select_related('author').filter(show_in_head=True)[:3]
        return ArticlePost.objects.select_related('author').published()


class ArticlePostDetailView(RetrieveAPIView):
    """Get article detail."""

    lookup_field = 'id'
    serializer_class = ArticlePostDetailSerializers
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ArticlePost.objects.published()


class ArticleCommentsCreateView(APIView):
    """Create comments."""
    serializer_class = ArticleCreateCommentsSerializers
    queryset = ArticleComments.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # new_captcha: CaptchaStore = CaptchaStore.generate_key()
        # captcha_image_urls = captcha_image_url(new_captcha)
        # return Response({'key': new_captcha, 'image_url': captcha_image_urls})
        return get_captcha()

    def post(self, request):
        ser_data = self.serializer_class(data=request.data, partial=True, context={'request': request})
        if ser_data.is_valid():
            # # Verify the CAPTCHA
            # captcha = self.request.data.get('captcha', None)
            # captcha_hash_key = self.request.data.get('key', None)
            # captcha_response: CaptchaStore = CaptchaStore.objects.filter(hashkey=captcha_hash_key).first()
            # if not captcha:
            #     return Response({'captcha': 'Captcha is required.'}, status=status.HTTP_400_BAD_REQUEST)
            # if captcha_response is None:
            #     return Response({'captcha': 'Captcha verification failed.'}, status=status.HTTP_400_BAD_REQUEST)
            # else:
            #     if captcha != captcha_response.response:
            #         return Response({'captcha': 'Captcha verification failed.'}, status=status.HTTP_400_BAD_REQUEST)
            #     if (captcha_response.expiration.minute - datetime.now(timezone.utc).minute) <= 4:
            #         CaptchaStore.delete(captcha_response)
            #         return Response({'captcha': 'Captcha verification failed.'}, status=status.HTTP_400_BAD_REQUEST)
            #
            # ser_data.create(ser_data.validated_data)
            # CaptchaStore.delete(captcha_response)
            # return Response('created successfully', status=status.HTTP_201_CREATED)
            return verify(request, ser_data)
        else:
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleCommentLikesCreateView(CreateAPIView):
    """Like a comment"""
    serializer_class = ArticleCommentLikesSerializers
    queryset = ArticleCommentsLikes.objects.all()
    permission_classes = (IsAuthenticated,)



class TagListView(ListAPIView):
    """List all tags."""
    serializer_class = ArticleTagSerializers
    queryset = ArticleTag.objects.all()
    permission_classes = (AllowAny,)