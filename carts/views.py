# Django Built-in modules
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

# Local Apps
from .cart import Cart
from .exceptions import CartException
from products.models import Variant
from coupon.models import DiscountCoupon
from coupon.models import DiscountException


def show(request):
    return render(request, 'cart/cart.html')


@csrf_exempt
def add(request):
    try:
        variant_id = request.POST.get('vid')
        variant = Variant.objects.get(pk=variant_id)
        quantity = request.POST.get('quantity',variant.order_limit_min)

        cart = Cart(request.session)
        cart.add(variant=variant, quantity=quantity)
        return JsonResponse({'status': 200, 'message': f"{str(_('به سبد خرید شما اضافه شد.'))}"})
    except CartException as cart_exception:
        return JsonResponse({'status': 500, 'message': str(cart_exception)})
    except ValueError as value_error:
        return JsonResponse({'status': 500, 'message': str(value_error)})
    except Exception as exception:
        return JsonResponse({'status': 500, 'message': _('خطایی رخ داد. لطفا مجددا تلاش کنید.')})


@csrf_exempt
def set_quantity(request):
    try:
        variant_id = request.POST.get('vid')
        quantity = request.POST.get('quantity', 1)
        variant = Variant.objects.get(pk=variant_id)

        cart = Cart(request.session)
        cart.set_quantity(variant=variant, quantity=quantity)
        return JsonResponse({'status': 200, 'message': f"{variant.product_name} {str(_('در سبد خرید شما تغییر یافت.'))}"})
    except CartException as cart_exception:
        return JsonResponse({'status': 500, 'message': str(cart_exception)})
    except Exception as exception:
        return JsonResponse({'status': 500, 'message': _('خطایی رخ داد. لطفا مجددا تلاش کنید.')})


@csrf_exempt
def remove(request):
    try:
        variant_id = request.POST.get('vid')
        cart = Cart(request.session)
        variant = Variant.objects.get(pk=variant_id)
        cart.remove(variant)
        return JsonResponse({'status': 200, 'message': f"{variant.product_name} {str(_('از سبد خرید شما حذف شد.'))}"})
    except CartException as cart_exception:
        return JsonResponse({'status': 500, 'message': str(cart_exception)})
    except Exception as exception:
        return JsonResponse({'status': 500, 'message': _('خطایی رخ داد. لطفا مجددا تلاش کنید.')})


@csrf_exempt
def apply_discount_coupon(request):
    try:
        discount_coupon = DiscountCoupon.objects.get(code=request.POST.get('discount_coupon').lower())
        cart = Cart(request.session)
        cart_detail = cart.detail
        discount_coupon.validation(
            amount=cart.total,
            products=cart_detail['products'],
            categories=cart_detail['categories'],
        )
        cart.apply_discount_coupon(discount_coupon=discount_coupon)
        return JsonResponse({'status': 200, 'message': _('کوپن تخفیف اعمال شد.')})
    except DiscountCoupon.DoesNotExist:
        return JsonResponse({'status': 403, 'message': _('کوپن تخفیف پیدا نشد.')})
    except DiscountException as exception:
        return JsonResponse({'status': 500, 'message': str(exception)})
    except CartException as cart_exception:
        return JsonResponse({'status': 500, 'message': str(cart_exception)})
    except Exception as exception:
        return JsonResponse({'status': 500, 'message': _('خطایی رخ داد. لطفا مجددا تلاش کنید.')})


@csrf_exempt
def remove_discount_coupon(request):
    try:
        cart = Cart(request.session)
        cart.remove_discount_coupon()
        return JsonResponse({'status': 200, 'message': _('کوپن تخفیف حذف شد.')})
    except CartException as cart_exception:
        return JsonResponse({'status': 500, 'message': str(cart_exception)})
    except Exception as exception:
        return JsonResponse({'status': 500, 'message': _('خطایی رخ داد. لطفا مجددا تلاش کنید.')})


@csrf_exempt
def add_payment(request):
    try:
        method = request.POST.get('method')
        cart = Cart(request.session)
        cart.add_payment(method=int(method))
        return JsonResponse({'status': 200, })
    except Exception as exception:
        return JsonResponse({'status': 500, 'message': _('خطایی رخ داد. لطفا مجددا تلاش کنید.')})


def load_cart_menu(request):
    return render(request, 'cart/cart_menu.html')
