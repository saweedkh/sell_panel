# Django Built-in modules
from django.urls import path
# Locals apps
from . import views

app_name = 'ajax'

urlpatterns = [
    # Cart
    path('cart/count/', views.cart_unique_count, name='cart_unique_count'),
    path('cart/items/', views.cart_items, name='cart_items'),
    path('cart/page/', views.cart_page, name='cart_page'),
    # Transportation
    path('cities/', views.load_cities, name='load_cities'),
    # Product
    path('product/comment/submit/<slug>/', views.comment_product_submit, name='comment_product_submit'),
    path('product/comment/reply/<slug>/', views.reply_product_submit, name='reply_product_submit'),
    # Blog
    path('post/comment/submit/<slug>/', views.comment_post_submit, name='comment_post_submit'),
    path('post/comment/reply/<slug>/', views.reply_post_submit, name='reply_post_submit'),
    # Bookmark
    path('bookmark/add/<post_id>/', views.bookmark_add, name='bookmark_add'),
    # Wishlist
    path('wishlist/add/<product_id>/', views.wishlist_add, name='wishlist_add'),
    # Address
    path('address/add/', views.address_add, name='address_add'),
    # Cache conflict
    path('cache/conflict/', views.cache_conflict, name='cache_conflict'),
    # News
    path('add-email/', views.add_email_to_news, name='add_email_to_news'),
    # Change Avatar 
    path('change-avatar/', views.change_avatar, name='change_avatar'),
]
