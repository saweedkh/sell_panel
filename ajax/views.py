# Django Built-in modules
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


# Local Apps
from news.forms import NewsForm
from news.models import News
from products.models import Product, ProductComment
from products.forms import AuthenticatedCommentForm as ProductAuthenticatedCommentForm, \
    AnonymousCommentForm as ProductAnonymousCommentForm
from accounts.models import User, Wishlist, Bookmark
from carts.cart import Cart
from transportation.models import Province
from blog.models import Post, BlogComment
from blog.forms import (
    AuthenticatedCommentForm as PostAuthenticatedCommentForm,
    AnonymousCommentForm as PostAnonymousCommentForm,
    AuthenticatedReplyForm as PostAuthenticatedReplyForm,
    AnonymousReplyForm as PostAnonymousReplyForm
)
from products.forms import (
    AuthenticatedCommentForm as ProductAuthenticatedCommentForm,
    AnonymousCommentForm as ProductAnonymousCommentForm,
    AuthenticatedReplyForm as ProductAuthenticatedReplyForm,
    AnonymousReplyForm as ProductAnonymousReplyForm
)
from accounts.forms import AddressForm, EditAvatarForm, EditProfileForm


def load_cities(request):
    try:
        province_id = request.GET.get('id_province')
        province = Province.objects.get(id=province_id)
        cities = province.cities.all()
    except (Province.DoesNotExist, ValueError):
        cities = []
    return TemplateResponse(request, "transportation/options.html", {"objects": cities})


def wishlist_add(request, product_id):
    if request.user.is_anonymous:
        return JsonResponse({'status': 405, 'message': _('برای ذخیره این محصول، وارد حساب کاربری خود شوید')})
    try:
        Wishlist.objects.get_or_create(user=request.user, product=Product.objects.get(id=product_id))
        return JsonResponse({'status': 200, 'message': _('به محصولات مورد علاقه ی شما اضافه شد')})
    except Exception as exception:
        return JsonResponse({'status': 500, 'message': f"{str(exception)}"})
    
    


@csrf_exempt
@require_POST
def comment_product_submit(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Exception:
        return JsonResponse({
            'status': 403,
            'message': _('مشکلی در ثبت نظر وجود دارد'),
        })

    if request.user.is_authenticated:
        form = ProductAuthenticatedCommentForm(request.POST)
    else:
        form = ProductAnonymousCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        if request.user.is_authenticated:
            comment.user = request.user
            comment.name = request.user.fullname
            comment.email = request.user.email
        comment.product = product
        comment.save()
        return JsonResponse({
            'status': 200,
            'message': _('نظر شما با موفقیت ثبت شد و پس از تایید مدیران نشان داده می شود'),
        })
    return JsonResponse({
        'status': 403,
        'message': _('مقادیر وارد شده را کنترل کنید'),
    })


@csrf_exempt
@require_POST
def reply_product_submit(request, slug):
    try:
        product = Product.objects.published().get(slug=slug)
        parent = ProductComment.accepted.get(id=request.POST.get('parent'))
        parent_type = request.POST.get('comment_type')
    except Exception as e:
        return JsonResponse({
            'status': 403,
            'message': _('مشکلی در ثبت نظر وجود دارد'),
        })

    if request.user.is_authenticated:
        form = ProductAuthenticatedCommentForm(request.POST)
    else:
        form = ProductAnonymousCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        if request.user.is_authenticated:
            comment.user = request.user
            comment.name = request.user.fullname
            comment.email = request.user.email
        comment.product = product
        comment.comment_type = parent_type
        comment.parent = parent
        comment.save()
        return JsonResponse({
            'status': 200,
            'message': _('نظر شما با موفقیت ثبت شد و پس از تایید مدیران نشان داده می شود'),
        })
    return JsonResponse({
        'status': 403,
        'message': _('مقادیر وارد شده را کنترل کنید'),
    })


@csrf_exempt
@require_POST
def comment_post_submit(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Exception:
        return JsonResponse({
            'status': 403,
            'message': _('مشکلی در ثبت نظر وجود دارد'),
        })

    if request.user.is_authenticated:
        form = PostAuthenticatedCommentForm(request.POST)
    else:
        form = PostAnonymousCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        if request.user.is_authenticated:
            comment.user = request.user
            comment.name = request.user.fullname
            comment.email = request.user.email
        comment.post = post
        comment.save()
        return JsonResponse({
            'status': 200,
            'message': _('نظر شما با موفقیت ثبت شد و پس از تایید مدیران نشان داده می شود'),
        })
    return JsonResponse({
        'status': 403,
        'message': _('مقادیر وارد شده را کنترل کنید'),
    })


@csrf_exempt
@require_POST
def reply_post_submit(request, slug):
    try:
        post = Post.objects.published().get(slug=slug)
        parent = BlogComment.accepted.get(id=request.POST.get('parent'))
    except Exception as e:
        return JsonResponse({
            'status': 403,
            'message': _('مشکلی در ثبت نظر وجود دارد'),
        })

    if request.user.is_authenticated:
        form = PostAuthenticatedCommentForm(request.POST)
    else:
        form = PostAnonymousCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        if request.user.is_authenticated:
            comment.user = request.user
            comment.name = request.user.fullname
            comment.email = request.user.email
        comment.post = post
        comment.parent = parent
        comment.save()
        return JsonResponse({
            'status': 200,
            'message': _('نظر شما با موفقیت ثبت شد و پس از تایید مدیران نشان داده می شود'),
        })
    return JsonResponse({
        'status': 403,
        'message': _('مقادیر وارد شده را کنترل کنید'),
    })


def cart_unique_count(request):
    _cart = Cart(request.session)
    # return HttpResponse(_cart.count)
    return render(request, 'ajax/cart-count.html')


@require_POST
@login_required
def address_add(request):
    form = AddressForm(request.POST)
    if form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.save()
        return JsonResponse({
            'status': 200,
            'message': _('آدرس اضافه شد'),
        })
    return JsonResponse({
        'status': 403,
        'message': _('مقادیر وارد شده را کنترل کنید'),
    })


def bookmark_add(request, post_id):
    if request.user.is_anonymous:
        return JsonResponse({'status': 405, 'message': _('برای ذخیره این پست، وارد حساب کاربری خود شوید')})
    try:
        _post = Post.objects.published().get(id=post_id)
        Bookmark.objects.get_or_create(user=request.user, post=_post)
        return JsonResponse({'status': 200, 'message': _(f'{_post.name} به لیست مطالعه شما اضافه شد ')})
    except Exception as exception:
        return JsonResponse({'status': 500, 'message': f"{str(exception)}"})


def cache_conflict(request):
    if request.user.is_authenticated:
        post_comment_form = PostAuthenticatedCommentForm()
        post_reply_form = PostAuthenticatedReplyForm()
    else:
        post_comment_form = PostAnonymousCommentForm()
        post_reply_form = PostAnonymousReplyForm()

    if request.user.is_authenticated:
        product_comment_form = ProductAuthenticatedCommentForm()
        product_reply_form = ProductAuthenticatedReplyForm()
    else:
        product_comment_form = ProductAnonymousCommentForm()
        product_reply_form = ProductAnonymousReplyForm()

    context = {'post_comment_form': post_comment_form, 'post_reply_form': post_reply_form,
               'product_comment_form': product_comment_form, 'product_reply_form': product_reply_form}
    return render(request, 'ajax/cache_conflict.html', context)


def cart_items(request):
    _cart = Cart(request.session)
    items_dic = dict()
    for item in _cart.items:
        items_dic[item.variant.pk] = item.quantity
    return JsonResponse(items_dic)


def cart_page(request):
    return render(request, 'ajax/cart-page.html' )




@require_POST
def add_email_to_news(request: HttpRequest):
    form = NewsForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        news_object, created = News.objects.get_or_create(email=email)            
        
        if not created:
            return JsonResponse({'status': 409, 'message': _('این ایمیل قبلاً در خبرنامه ثبت شده است')})
        
        if request.user.is_authenticated:
            news_object.user = request.user
            news_object.save()

        return JsonResponse({'status': 200, 'message': _('ایمیل شما در خبرنامه ثبت شد')})
    
    return JsonResponse({'status': 403, 'message': _('مقادیر وارد شده را کنترل کنید')})
    
@require_http_methods(['POST'])
def change_avatar(request):
    
    form = EditAvatarForm(request.POST, request.FILES)
    if form.is_valid():
        user_profile = User.objects.get(pk=request.user.pk)
        user_profile.avatar = request.FILES.get('avatar')
        user_profile.save()
        return JsonResponse({'status': 200, 'message': _('تصویر پروفایل شما با موفقیت به روز شد')})
    
    return JsonResponse({'status': 400, 'message': _('مقادیر وارد شده را کنترل کنید')})