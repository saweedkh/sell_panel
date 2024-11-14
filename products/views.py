# Django Built-in modules
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from products.serializers import ProductCommentSerializer, ProductDetailSerializers, ProductSerializers

# Locals apps
from .filters import ProductFilter, ProductListPageFilter
from .models import (
    Product,
    Variant,
    ProductSpecification,
    ProductComment as Comment,
    Brand,
    ProductSettings,
    ProductComment,
)
from .forms import (
    SelectAttributeForm,
    AuthenticatedCommentForm,
    AnonymousCommentForm,
    AuthenticatedReplyForm,
    AnonymousReplyForm,
)
from .utils import ProductSortChoices, sort_products
from utils.paginator import paginator


from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

def brand(request, slug):
    _brand = get_object_or_404(Brand, slug=slug, page_display_status=Brand.PUBLISH)
    qs = Product.objects.published().filter(brand=_brand)
    product_filters = ProductFilter(request.GET, queryset=qs, brand=_brand)
    products = paginator(request=request, qs=product_filters.qs,
                         per_page=ProductSettings.objects.get_first().paginator_number)
    context = {'products': products, 'brand': _brand, 'product_filters': product_filters}
    return render(request, 'product/brand.html', context)


@csrf_exempt
def product(request, slug):
    _product = get_object_or_404(Product, slug=slug, page_display_status=Product.PUBLISH)

    variant_attribute_values = request.POST.getlist('attribute__value_ids[]')
    if variant_attribute_values:
        try:
            variant = _product.find_variant_by_attribute_values(selected=[int(v) for v in variant_attribute_values])
        except Variant.DoesNotExist:
            variant = _product.default_variant
    else:
        variant = _product.default_variant

    select_attribute_form = SelectAttributeForm(
        product_attributes=_product.get_attributes,
        default_variant_pk=variant.pk if variant else None,
        attributes_input_types=_product.get_attributes_input_types,
    )

    if request.user.is_authenticated:
        comment_form = AuthenticatedCommentForm()
        reply_form = AuthenticatedReplyForm()
    else:
        comment_form = AnonymousCommentForm()
        reply_form = AnonymousReplyForm()

    comments_qs = _product.productcomment_set.filter(status=Comment.ACCEPT)
    comments = comments_qs.filter(comment_type=Comment.COMMENT)
    qas = comments_qs.filter(comment_type=Comment.QA)
    product_specifications = ProductSpecification.objects.filter(product_id=_product.id, ).select_related(
        'general_attribute', ).prefetch_related('attribute_value', )
    slider_position, product_gallery = _product.get_gallery(variant)
    context = {'product': _product, 'variant': variant, 'select_attribute_form': select_attribute_form,
               'comment_form': comment_form, 'comments': comments, 'product_specifications': product_specifications,
               'qas': qas, 'reply_form': reply_form, 'product_gallery': product_gallery,
               'slider_position': slider_position}
    return render(request, 'product/product.html', context)


@staff_member_required
def reply_comment(request, parent_id):
    comment = get_object_or_404(Comment, id=parent_id)
    if request.method == 'POST':
        form = AuthenticatedCommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.product = comment.product
            reply.user = request.user
            reply.parent = comment
            reply.name = request.user.fullname
            reply.email = request.user.email
            reply.save()
            messages.success(request, _('پاسخ شما با موفقیت ثبت شد'))
            return redirect(comment.admin_edit_absolute_url())
    else:
        form = AuthenticatedCommentForm()
    context = {'form': form, 'comment': comment}
    return render(request, 'comment/reply_admin.html', context)


def product_preview(request, product_id):
    _product = get_object_or_404(Product, id=product_id, page_display_status=Product.PUBLISH)
    comments_count = _product.productcomment_set.filter(status=ProductComment.ACCEPT).count()

    variant_attribute_values = request.POST.getlist('attribute__value_ids[]')
    if variant_attribute_values:
        try:
            variant = _product.find_variant_by_attribute_values(selected=[int(v) for v in variant_attribute_values])
        except Variant.DoesNotExist:
            variant = _product.default_variant
    else:
        variant = _product.default_variant
    select_attribute_form = SelectAttributeForm(
        product_attributes=_product.get_attributes,
        default_variant_pk=variant.pk if variant else None,
        attributes_input_types=_product.get_attributes_input_types,
    )
    context = {'product': _product, 'variant': variant, 'comments_count': comments_count,
               'select_attribute_form': select_attribute_form}
    return render(request, 'product/inc/product_preview.html', context)


@csrf_exempt
def select_attribute(request):
    product_id = int(request.POST.get('product_id'))
    context = {'error': True}

    if product_id:
        try:
            _product = Product.objects.get(id=product_id, page_display_status=Product.PUBLISH)
            variant_attribute_values = request.POST.getlist('attribute__value_ids[]')
            if variant_attribute_values:
                try:
                    variant = _product.find_variant_by_attribute_values(
                        selected=[int(v) for v in variant_attribute_values])
                except Variant.DoesNotExist:
                    variant = _product.default_variant
            else:
                variant = _product.default_variant

            select_attribute_form = SelectAttributeForm(
                product_attributes=_product.get_attributes,
                default_variant_pk=variant.pk if variant else None,
                attributes_input_types=_product.get_attributes_input_types,
                prefix=f'p-{product_id}'
            )
            context = {'product': _product, 'variant': variant, 'select_attribute_form': select_attribute_form,
                       'error': False}
        except Product.DoesNotExist as e:
            pass

    return render(request, 'product/inc/product_card_overlay.html', context)


def fill_related_products(request, product_id):
    _product = get_object_or_404(Product, id=product_id)
    new_related_products = _product.get_related_products()
    existing_related_products = _product.related_products.all()
    final = set(new_related_products) - set(list(existing_related_products))
    data = [{'id': rp.id, 'name': rp.name, 'url': rp.get_absolute_url()} for rp in final]
    return JsonResponse({'data': data, 'status': 200})




class ProductView(ListAPIView):
    serializer_class = ProductSerializers
    queryset = Product.objects.published()

class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductDetailSerializers
    lookup_field = 'id'
    
    def get_queryset(self):
        return Product.objects.published()
    
    
    
    
class ProductCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]  
    serializers_class = ProductCommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)