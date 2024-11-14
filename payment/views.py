# Django Built-in modules
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.utils.translation import gettext_lazy as _
from django.http import (
    Http404,
    HttpResponseRedirect,
    JsonResponse,
)

# Local Apps
from gateways.models.banks import Bank
from gateways.models.enum import PaymentStatus
from orders.models import Invoice, Order
from orders.serializers import OrderSerializer
from payment.serializers import InvoiceSerializers
from .forms import ReceiptForm
from .models import PaymentSetting
from gateways import models as bank_models, default_settings as settings

# Third Party Packages
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from  rest_framework.permissions import IsAuthenticated




class GetInvoiceView(GenericAPIView):
    
    serializer_class = InvoiceSerializers

    
    def get(self, request , *args, **kwargs):
        tracking_code = request.GET.get('tc')
        
        if not tracking_code:
            return Response({'status': 400, 'msg': _('کد رهگیری اجباری است.')}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.filter(tracking_code=tracking_code).first()
        if not order:
            return Response({'status': 404, 'msg': _('سفارش یافت نشد.')}, status=status.HTTP_404_NOT_FOUND)
        
        
        
        
        
        if int(order.payable) == 0:
            order.paid = True
            order.order_status = order.DONE
            order.save()
            serializer = self.serializer_class(order,)
            invoice = Invoice.create(order)
            return Response(serializer.data)
        else:
            bank = get_object_or_404(Bank, tracking_code=tracking_code)

            if bank.status == PaymentStatus.COMPLETE:
                if not order.paid:
                    order.paid = True
                    order.order_status = order.AWAITING_CHECK
                    order.deposit_date = bank.updated
                    order.save()
                    invoice = Invoice.create(order)
 
                serializer = self.serializer_class(order,)
                return Response(serializer.data)
            else:
                serializer = self.serializer_class(order,)
                serializer.data['url'] = order.payment_order_link
                return Response(serializer.data)
            

class PaymentOrder(GenericAPIView): 
    
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, tracking_code, *args, **kwargs):
        order = get_object_or_404(Order, tracking_code=tracking_code)
        if not order.is_payable:
            return Response({'msg' : _("سفارش مورد نظر قابل پرداخت نمی‌باشد")}, status=status.HTTP_400_BAD_REQUEST)
        
        url = order.go_to_gateway(request=request)
        if isinstance(url, str) and url.startswith('http'):
            return Response({'url' : url}, status=status.HTTP_200_OK)

        return Response({'msg' : str(url) }, status=status.HTTP_400_BAD_REQUEST)
    
    

    
def payment_invoice(request, tracking_code):
    invoice = get_object_or_404(Invoice, tracking_code=tracking_code)
    
    url = invoice.payment(request=request)
    if type(url) == HttpResponseRedirect:
        return JsonResponse({'status': 400})
    return redirect(url)



def payment_order(request, tracking_code):
    order = get_object_or_404(Order, tracking_code=tracking_code)
    if not order.is_payable:
        raise Http404
    return order.go_to_gateway(request=request)





def callback_gateway(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    print('call_back = ', tracking_code)
    if not tracking_code:
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        raise Http404

    order = get_object_or_404(Order, pk=bank_record.object_id)

    if not order.is_payable:
        return redirect('pages:home')

    if bank_record.is_success:
        order.complete_the_order(payment_method=order.payment_method, cart=Cart(request.session))
        return redirect('payment:success', order.tracking_code, order.uuid)

    SendSMSWithPattern(
        OrderStatusSMS.FAILED_PAYMENT,
        str(order.mobile_number.national_number),
        {'fname': order.first_name, 'lname': order.last_name, 'orderid': order.tracking_code},
    ).send()

    return redirect('payment:failed', order.tracking_code, order.uuid)


def upload_bank_receipt(request, tracking_code):
    order = get_object_or_404(Order, tracking_code=tracking_code)
    if order.is_payable:
        try:
            order.check_transfer_conditions(cart=Cart(request.session))
            order.receipt_received()

            setting = PaymentSetting.objects.get_first()
            cards = setting.card_set.active()
            amount = order.payable

            if request.method == 'POST':
                form = ReceiptForm(request.POST, files=request.FILES)
                if form.is_valid():
                    new_receipt = form.save(commit=False)
                    new_receipt.order = order
                    new_receipt.amount = amount
                    new_receipt.save()
                    return redirect('payment:success', order.tracking_code, order.uuid)
            else:
                form = ReceiptForm
            context = {'form': form, 'cards': cards, 'setting': setting, 'amount': amount,
                       'tracking_code': tracking_code}
            return render(request, 'payment/card_transfer.html', context)
        except:
            return redirect('payment:failed', order.tracking_code, order.uuid)
    else:
        return redirect('pages:home')


@login_required
def withdraw_from_wallet(request, tracking_code):
    order = get_object_or_404(Order, tracking_code=tracking_code)
    if order.is_payable:
        try:
            order.check_wallet_conditions(cart=Cart(request.session), user=request.user)
            wallet = request.user.wallet
            wallet.transaction(amount=order.payable, _type=wallet.WITHDRAW)
            order.complete_the_order(payment_method=Order.WALLET)
            return redirect('payment:success', order.tracking_code, order.uuid)
        except:
            return redirect('payment:failed', order.tracking_code, order.uuid)
    else:
        return redirect('pages:home')


def post_paid_payment(request, tracking_code):
    order = get_object_or_404(Order, tracking_code=tracking_code)
    if order.is_payable:
        try:
            order.check_post_paid_conditions(cart=Cart(request.session))
            setting = PaymentSetting.objects.get_first()
            if setting.prepayment_status_for_post_paid:
                return order.go_to_gateway_post_paid(request=request)
            else:
                order.waiting_to_confirm_order()
                return redirect('payment:success', order.tracking_code, order.uuid)
        except:
            return redirect('payment:failed', order.tracking_code, order.uuid)
    else:
        return redirect('pages:home')


def success_result(request, tracking_code, order_uuid):
    order = get_object_or_404(Order, tracking_code=tracking_code, uuid=order_uuid)
    context = {'order': order}
    return render(request, 'payment/transaction_success_result.html', context)


def failed_result(request, tracking_code, order_uuid):
    order = get_object_or_404(Order, tracking_code=tracking_code, uuid=order_uuid)
    context = {'order': order}
    return render(request, 'payment/transaction_failed_result.html', context)


def exception(request, tracking_code, order_uuid):
    order = get_object_or_404(Order, tracking_code=tracking_code, uuid=order_uuid)
    context = {'order': order}
    return render(request, 'payment/transaction_exception.html', context)
