from .cart import Cart


def cart_unique_count(request):
    _cart = Cart(request.session)
    return {'cart_unique_count': _cart.unique_count}


def cart(request):
    return {'cart': Cart(request.session)}