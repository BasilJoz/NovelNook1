from django.urls import path
from . import views
urlpatterns = [
    path('cart',views.cart,name='cart' ),
    path('add_cart/<int:book_id>',views.add_cart,name='add_cart' ),
    path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('useraddress', views.useraddress, name='useraddress'),
    path('add_address', views.add_address, name='add_address'),
    path('edit_address/<int:edit_id>', views.edit_address, name='edit_address'),
    path('delete_address/<int:del_id>', views.delete_address, name='delete_address'),
    path('checkout',views.checkout, name='checkout'),
    path('order_summary/<int:address_id>/<int:order_id>', views.order_summary, name='order_summary'),
    path('my_orders',views.my_orders, name='my_orders'),
    path('cancel_order/<int:order_id>/<int:product_id>', views.cancel_order, name='cancel_order'),
    path('update_cart_item_quantity', views.update_cart_item_quantity, name='update_cart_item_quantity'),
    path('get_cart_item_count', views.get_cart_item_count, name='get_cart_item_count'),
    path('coupons_details', views.coupons_details, name='coupons_details'),
    path('remove_coupon', views.remove_coupon, name='remove_coupon'),
    path('hello', views.hello, name='hello'),
    path('payment/<int:address_id>', views.payment, name='payment'),
    path('razor/<int:address_id>/<str:final_total>', views.razor, name="razor"),
    path('wishlist', views.wishlist, name="wishlist"),

    
]
