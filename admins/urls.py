from django.urls import path
from admins import views

urlpatterns = [
    # path('admin',views.handleadmin,name='admin'),
    path('signin',views.hanglesignin,name='signin'),
    path('index',views.handleindex,name='index'),
    path('users',views.handleuser,name='users'),
    path('block_user/<int:id>/',views.handleblock,name='block_user'),
    path('unblock_user/<int:id>',views.handleunblock,name='unblock_user'),
    path('category',views.handlecategory,name='category'),
    path('add_category',views.add_category,name='add_category'),
    path('edit_category/<int:id>',views.edit_category,name='edit_category'),
    path('delete_category/<int:id>',views.delete_category,name='delete_category'),
    path('products',views.products,name='products'),
    path('add_products',views.add_products,name='add_products'),
    path('edit_products/<int:book_id>',views.edit_products,name='edit_products'),
    path('delete_products/<int:book_id>',views.delete_products,name='delete_products'),
    path('undelete_products/<int:book_id>',views.undelete_products,name='undelete_products'),
    path('logout',views.handlelogout,name='handlelogout'),
    path('userorders',views.userorders,name='userorders'),
    path('userorderitems/<int:id>',views.userorderitems,name='userorderitems'),
    path('orderstatus/<int:id>',views.orderstatus,name='orderstatus'),
    path('coupons',views.coupons,name='coupons'),
    path('add_coupons',views.add_coupons,name='add_coupons'),
    path('edit_coupons/<int:id>',views.edit_coupons,name='edit_coupons'),
    path('delete_coupons/<int:id>',views.delete_coupons,name='delete_coupons'),
   
]
