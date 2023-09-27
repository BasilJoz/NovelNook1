from django.urls import path
from logins import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.handlelogin,name='login'),
    path('signup/',views.handlesignup,name='signup'),
    path('Otp/<str:phone>,<int:id>', views.Otp,name='Otp'),
    path('Logout', views.Logout,name='Logout'),
    path('handleshop/', views.handleshop,name='handleshop'),
    path('hanldesingleproduct/<int:product_id>', views.hanldesingleproduct,name='hanldesingleproduct'),
    
]
