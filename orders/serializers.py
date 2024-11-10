from rest_framework import serializers

from coupon.models import DiscountCoupon, DiscountException
from products.models import Variant
from .models import Order, OrderItem

from django.db.transaction import atomic



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['variant', 'quantity',]  

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    discount_code = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = [
            'tracking_code',
            'first_name', 'last_name', 'mobile_number', 'email', 'payable',
            'province_id', 'city_id', 'address', 'postal_code', 'note',
            'discount_code', 'payment_method', 'items', 'order_items',
        ]
        read_only_fields = (
            'tracking_code',
            'payable',
        )
        
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        discount_code = validated_data.pop('discount_code', None)
        

        # اگر کد تخفیف موجود باشد، نمونه‌ی مدل DiscountCoupon را بگیریم
        discount_coupon = None
        if discount_code:
            try:
                discount_coupon = DiscountCoupon.objects.get(code=discount_code)
                # اعتبارسنجی کوپن تخفیف
                discount_coupon.validation(amount=None, products=[item['variant'].product for item in items_data])
                validated_data['discount_code'] = discount_coupon
            except DiscountCoupon.DoesNotExist:
                raise serializers.ValidationError({"discount_code": "کد تخفیف معتبر نیست."})
            except DiscountException as e:
                raise serializers.ValidationError({"discount_code": str(e)})


        with atomic():
            order = Order.objects.create(**validated_data)
            payable = 0
            items = []
            for item in items_data:
                variant = Variant.objects.get(id=item['variant'].id)
                payable += variant.final_price * item['quantity']
                item_data = {
                    'order': order,
                    'variant': variant,
                    'quantity': item['quantity'],
                    'price': variant.price,
                    'total_price': variant.final_price,
                    'amount_payable': variant.final_price * item['quantity'],
                }
                items.append(OrderItem(**item_data))

            OrderItem.objects.bulk_create(items)
            order.payable = payable
            order.save()
            return order




class OrderListSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = (
            'tracking_code',
            'order_status',
            'payable',
            'paid',
            
        )
        
        
class OrderDetailSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = (
            'tracking_code',
            'order_status',
            'payable',
            'paid',
            'reference_code',
            'postal_tracking_code',
            'first_name',
            'last_name',
            'mobile_number',
            'email',
            'province_id',
            'province',
            'city_id',
            'city',
            'address_id',
            'address',
            'postal_code',
            'note',
            'packing_type',
            'commodity_prices',
            'total_discount',
            'discount_amount',
            'prepayment',
            'payable',
            'payment_method',
            'paid',
            'deposit_date',
            
        )