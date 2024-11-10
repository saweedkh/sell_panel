from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from decimal import Decimal

from . import module_loading
from . import settings as carton_settings
from coupon.models import DiscountCoupon
from payment.models import PaymentSetting
from orders.models import Order


class CartItem(object):
    """
    A cart item, with the associated variant, its quantity and its price.
    """

    def __init__(self, variant, quantity):
        self.variant = variant
        self.quantity = int(quantity)
        self.final_price = Decimal(variant.final_price)
        self.price = Decimal(variant.price)
        self.discount = Decimal(variant.discount) if variant.discount else 0

    def __repr__(self):
        return u'CartItem Object (%s)' % self.variant

    def to_dict(self):
        return {
            'pk': self.variant.pk,
            'quantity': self.quantity,
            'final_price': str(self.final_price),
            'price': str(self.price),
            'discount': str(self.discount),
        }

    @property
    def subtotal(self):
        """
        Subtotal for the cart item.
        """
        return self.price * self.quantity

    @property
    def final_subtotal(self):
        """
        Subtotal for the cart item after discount.
        """
        return self.final_price * self.quantity

    @property
    def subdiscount(self):
        """
        Discount for the cart item.
        """
        return self.discount * self.quantity


class Cart(object):
    """
    A cart that lives in the session.
    """

    def __init__(self, session, session_key=None):
        self._items_dict = {}
        self.session = session
        self.session_key = session_key or carton_settings.CART_SESSION_KEY
        self.discount = self.session.get('discount')
        self.shipment = self.session.get('shipment')
        default_payment = {
            'enable': False,
            'percent': 0,
        }
        self.payment = self.session.get('payment', default_payment)

        # If a cart representation was previously stored in session, then we
        if self.session_key in self.session:
            # rebuild the cart object from that serialized representation.
            cart_representation = self.session[self.session_key]
            ids_in_cart = cart_representation.keys()
            variants_queryset = self.get_queryset().filter(pk__in=ids_in_cart)
            for variant in variants_queryset:
                item = cart_representation[str(variant.pk)]
                self._items_dict[variant.pk] = CartItem(variant, item['quantity'], )

        # Update Discount Amount (TODO: Delete this snippet)
        if self.discount:
            pk = self.discount['pk']
            ds = DiscountCoupon.objects.get(pk=pk)
            self.session['discount'] = {
                'pk': ds.pk,
                'description': ds.get_description,
                'describe_amount': 1,
                'amount': ds.calculate_discount(amount=self.final_total_items),
            }

    def __contains__(self, variant):
        """
        Checks if the given variant is in the cart.
        """
        return variant in self.variants

    def get_product_variant_model(self):
        return module_loading.get_product_variant_model()

    def filter_product_variants(self, queryset):
        """
        Applies lookup parameters defined in settings.
        """
        lookup_parameters = getattr(settings, 'CART_PRODUCT_LOOKUP', None)
        if lookup_parameters:
            queryset = queryset.filter(**lookup_parameters)
        return queryset

    def get_queryset(self):
        variant_model = self.get_product_variant_model()
        queryset = variant_model._default_manager.all()
        queryset = self.filter_product_variants(queryset)
        return queryset

    def update_session(self):
        """
        Serializes the cart data, saves it to session and marks session as modified.
        """
        self.session[self.session_key] = self.cart_serializable
        self.session.modified = True

    def add(self, variant, quantity=1):
        """
        Adds or creates variants in cart. For an existing variant,
        the quantity is increased and the price is ignored.
        """
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError(_('حداقل تعداد مجاز برای افزودن به سبد خرید برابر با ۱ است.'))
        if variant in self.variants:
            total_quantity = self._items_dict[variant.pk].quantity + quantity
            if variant.order_limit_max:
                if total_quantity > variant.order_limit_max:
                    raise ValueError(_(f'حداکثر تعداد مجاز برای افزودن محصول {variant.product.name} به سبد خرید برابر با {variant.order_limit_max} است.'))
                
            variant.validation_to_add_to_cart(quantity=total_quantity)
            self._items_dict[variant.pk].quantity = total_quantity
        else:
            variant.validation_to_add_to_cart(quantity=quantity)
            self._items_dict[variant.pk] = CartItem(variant, quantity)
        self.update_session()

    def remove(self, variant):
        """
        Removes the variant.
        """
        if variant in self.variants:
            del self._items_dict[variant.pk]
            self.update_session()

    def remove_single(self, variant):
        """
        Removes a single variant by decreasing the quantity.
        """
        if variant in self.variants:
            if self._items_dict[variant.pk].quantity <= 1:
                # There's only 1 variant left so we drop it
                del self._items_dict[variant.pk]
            else:
                self._items_dict[variant.pk].quantity -= 1
            self.update_session()

    def clear(self):
        """
        Removes all items.
        """
        self._items_dict = {}
        if self.session.get('discount'):
            self.session['discount'] = None
        if self.session.get('shipment'):
            self.session['shipment'] = None
        if self.session.get('payment'):
            self.session['payment'] = {
                'enable': False,
                'percent': 0,
            }
        self.update_session()

    def set_quantity(self, variant, quantity):
        """
        Sets the variant's quantity.
        """
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError(_('هنگام بروزرسانی سبد خرید، تعداد باید مثبت باشد'))
        if variant in self.variants:
            variant.validation_to_add_to_cart(quantity=quantity)
            self._items_dict[variant.pk].quantity = quantity
            if self._items_dict[variant.pk].quantity < 1:
                del self._items_dict[variant.pk]
            self.update_session()

    @property
    def items(self):
        """
        The list of cart items.
        """
        return self._items_dict.values()

    @property
    def cart_serializable(self):
        """
        The serializable representation of the cart.
        For instance:
        {
            '1': {'variant_pk': 1, 'quantity': 2, price: '9.99'},
            '2': {'variant_pk': 2, 'quantity': 3, price: '29.99'},
        }
        Note how the variant pk servers as the dictionary key.
        """
        cart_representation = {}
        for item in self.items:
            # JSON serialization: object attribute should be a string
            variant_id = str(item.variant.pk)
            cart_representation[variant_id] = item.to_dict()
        return cart_representation

    @property
    def items_serializable(self):
        """
        The list of items formatted for serialization.
        """
        return self.cart_serializable.items()

    @property
    def order_items(self):
        """
        Prepare and serializable items for order item model.
        """
        order_items = list()
        for item in self.items:
            variant = item.variant
            product = variant.product
            order_items.append(
                {
                    'product_id': variant.product_id,
                    'product_category': product.category.first(),
                    'brand_id': product.brand_id,
                    'variant_id': variant.id,
                    'attribute_value_id': variant.attribute_value_id,
                    'name': variant.variant_descriptor,
                    'quantity': item.quantity,
                    'price': variant.price,
                    'discount': variant.discount,
                    'total_price': item.subtotal,
                    'total_discount': item.subdiscount,
                    'amount_payable': item.final_subtotal,
                }
            )
        return order_items

    @property
    def count(self):
        """
        The number of items in cart, that's the sum of quantities.
        """
        return sum([item.quantity for item in self.items])

    @property
    def unique_count(self):
        """
        The number of unique items in cart, regardless of the quantity.
        """
        return len(self._items_dict)

    @property
    def is_empty(self):
        return self.unique_count == 0

    @property
    def variants(self):
        """
        The list of associated variants.
        """
        return [item.variant for item in self.items]

    @property
    def detail(self):
        """
        The list of associated products and detailt.
        """
        _detail = {'products': [], 'categories': []}
        for item in self.items:
            product = item.variant.product
            _detail['products'].append(product)
            [_detail['categories'].append(category) for category in product.category.all()]
        return _detail

    @property
    def total_items(self):
        """
        The total value of all items in the cart before discount.
        """
        return sum([item.subtotal for item in self.items])

    @property
    def final_total_items(self):
        """
        The total value of all items in the cart after discount.
        """
        return sum([item.final_subtotal for item in self.items])

    @property
    def total_profit(self):
        """
        The total profit of all items in the cart plus discount amount.
        """
        profit = sum([item.subdiscount for item in self.items])
        if self.discount:
            profit += self.discount.get('amount', 0)
        total_items = self.total_items
        return profit if profit < total_items else total_items

    @property
    def total_profit_cart_page(self):
        """
        The total profit of all items in the cart in cart page.
        """
        profit = sum([item.subdiscount for item in self.items])
        return profit

    @property
    def profit_percent(self):
        """
        The total profit percent of all items in the cart plus discount amount.
        """
        # percent = round(100 - ((self.total_price_in_cart - self.total_profit) / self.total_price_in_cart) * 100)
        percent = round(100 - ((self.total_items - self.total_profit) / self.total_items) * 100)
        return 100 if percent > 100 else percent

    @property
    def profit_percent_cart_page(self):
        """
        The total profit percent of all items in the cart plus discount amount in cart page.
        """
        percent = round(100 - ((self.total_items - self.total_profit_cart_page) / self.total_items) * 100)
        return 100 if percent > 100 else percent

    @property
    def total(self):
        total = self.total_price_in_cart
        if self.shipment:
            total += self.shipment.get('price', 0)
        if self.payment.get('enable', False):
            total = int((total / 100) * self.payment.get('percent', 0))
        total = 0 if total < 0 else total
        return total

    @property
    def total_price_in_cart(self):
        total = self.final_total_items
        if self.discount:
            total -= self.discount.get('amount', 0)
        total = 0 if total < 0 else total
        return total

    def apply_discount_coupon(self, discount_coupon):
        self.session['discount'] = {
            'pk': discount_coupon.pk,
            'description': discount_coupon.get_description,
            'describe_amount': 1,
            'amount': discount_coupon.calculate_discount(amount=self.final_total_items),
        }

    @property
    def discount_cart_page(self):
        if self.discount:
            pk = self.discount['pk']
            ds = DiscountCoupon.objects.get(pk=pk)
            return ds.calculate_discount(amount=self.final_total_items)
        return 0

    @property
    def payable_cart_page(self):
        return self.final_total_items - self.discount_cart_page

    def remove_discount_coupon(self):
        self.session['discount'] = None

    def add_payment(self, method):
        """
        Saves the payment method to session.
        """
        setting = PaymentSetting.objects.get_first()
        self.session['payment'] = {
            'enable': True if Order.POST_PAID == method and setting.prepayment_status_for_post_paid else False,
            'percent': setting.prepayment_percentage if setting.prepayment_status_for_post_paid else 0,
        }

    def validation_before_payment(self, request):
        invalids = list()
        for item in self.items:
            exception = item.variant.validation_before_payment(quantity=item.quantity)
            if exception:
                messages.error(request, exception)
                invalids.append(item.variant)
        [self.remove(i) for i in invalids]
        return True if len(invalids) == 0 else False
