# Django Built-in modules
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


from orders.serializers import OrderDetailSerializers, OrderListSerializers, OrderSerializer
from products.models import Variant

# Locals apps
from .forms import OrderForm, OrderTrackingForm
from .models import (
    Order,
    Invoice,
)
from .utils import (
    get_client_ip,
    get_user_agent,
)
# from account.forms import AddressForm
from django.conf import settings



from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response




def billing(request):
    cart = Cart(request.session)
    if cart.is_empty:
        return redirect('carts:show')

    if request.method == 'POST':
        order_form = OrderForm(request.POST, request=request, cart=cart)
        if order_form.is_valid():

            if not cart.validation_before_payment(request):
                return redirect('carts:show')

            order = Order.create(user=request.user, order_form_cleaned_data=order_form.cleaned_data, cart=cart)
            order.user_ip = get_client_ip(request)
            order.user_agent = get_user_agent(request)
            order.save()
            print('pre payment ----------> ')
            return order.choose_payment_method(request=request)
    else:
        order_form = OrderForm(request=request, cart=cart)

    # address_form = AddressForm(request=request)
    # addresses = AddressForm()
    context = {'order_form': order_form,}
    return render(request, 'order/checkout.html', context)


def tracking(request):
    if request.user.is_authenticated:
        return redirect('account:history')

    if request.method == 'POST':
        form = OrderTrackingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            mobile_number = cd.get('mobile_number')
            tracking_code = cd.get('tracking_code')
            order = Order.objects.filter(
                Q(mobile_number=mobile_number) & (Q(tracking_code=tracking_code) | Q(reference_code=tracking_code))
            )
            if order.exists():
                order = order.first()
                order_items = order.orderitem_set.select_related('product').all()
                context = {'order': order, 'order_items': order_items}
                return render(request, 'order/order-detail.html', context)
            messages.error(
                request,
                _('متاسفانه نتیجه ای پیدا نشد. لطفا از درست بودن کد پیگیری یا شماره تلفن اطمینان حاصل کنید.'), 'danger'
            )
            return redirect('orders:tracking')
    else:
        form = OrderTrackingForm()

    context = {'form': form}
    return render(request, 'order/tracking.html', context)


def invoice(request, invoice_id):
    _invoice = get_object_or_404(Invoice, pk=invoice_id)
    invoice_items = _invoice.invoiceitem_set.all()
    page_title = _('مشاهده پیش فاکتور') if _invoice.order.is_payable else _('مشاهده صورتحساب')
    context = {'invoice': _invoice, 'invoice_items': invoice_items, 'site_url': settings.SITE_DOMAIN,
               'page_title': page_title}
    return render(request, 'order/invoice.html', context)


@login_required
def thermal_printer_invoice(request, invoice_id):
    _invoice = get_object_or_404(Invoice, pk=invoice_id)
    invoice_items = _invoice.invoiceitem_set.all()
    context = {'invoice': _invoice, 'invoice_items': invoice_items, 'site_url': settings.SITE_DOMAIN}
    return render(request, 'order/thermal_printer_invoice.html', context)


@staff_member_required
def create_invoice(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    _invoice = Invoice.create(order)
    return redirect(_invoice.get_absolute_url())



def order_review(request, order_uuid):
    if request.method == 'POST':
        return redirect('payment:payment_order', order_uuid)

    order = get_object_or_404(Order, uuid=order_uuid)
    if not order.is_payable:
        raise Http404

    context = {'order': order}
    return render(request, 'order/review_order.html', context)





class CreateOrderView(GenericAPIView):
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            items_data = request.data.get('items')
            error_variant = {}
            for item in items_data:
                variant_id = item.get('variant')
                quantity = item.get('quantity')

                try:
                    variant = Variant.objects.get(id=variant_id)
                except Variant.DoesNotExist:
                    error_variant[variant_id] = Response({'error': 'کالای مورد نظر وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'error': 'کالای مورد نظر وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)
                
                msg =  variant.validation_before_payment(quantity) 
                if  msg != None:
                    return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
                

            order = serializer.save(user=request.user, user_agent=get_user_agent(request), user_ip=get_client_ip(request))
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
class OrderListView(ListAPIView):
    serializer_class = OrderListSerializers 
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ('created',)
    filterset_fields = ('paid',)
    search_fields = ('tracking_code',)
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    
    
class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderDetailSerializers
    lookup_field = 'tracking_code'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    