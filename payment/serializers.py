from rest_framework import serializers

from orders.models import Order

class InvoiceSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = (
           'tracking_code',
            'first_name',
            'last_name',
            'mobile_number',
            'paid',
            'payable',
            'note',
            
            
        )
        