# Django Built-in Modules
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

# Local apps
from .models import DiscountCoupon
from .utils import generate_code


@staff_member_required
def generate_discount_coupon(request):
    if request.method == 'GET':
        code = generate_code()
        counter = 0

        while DiscountCoupon.objects.filter(code=code).exists() and counter < 3:
            code = generate_code()
            counter += 1

        return JsonResponse({
            'status': 200,
            'code': code,
        })

    else:
        return JsonResponse({'status': 500})



