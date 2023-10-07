from django.db import models
from logins.models import user_details
from admins.models import books,Coupon
from  logins.models import Address
from django.utils import timezone

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(user_details,on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon,null=True,blank=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"cart for {self.user.username}"

class CartItems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    book = models.ForeignKey(books,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.book.title} in cart for {self.cart.user.username}" 
    
    
class Order(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    order_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price_shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def _str_(self):
        return f"Order #{self.id} by {self.user.username} on {self.order_date}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(books, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_status = models.CharField(max_length=20,
        choices=[
            ("Order Placed", "Order Placed"),
            ("Shipped", "Shipped"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled"),
        ],
        default="Order Placed",
    )

    def _str_(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.id}"


class Wishlist(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    books = models.ManyToManyField(books, related_name='wishlists')

    def __str__(self):
        return f'Wishlist of {self.user.username}'
   
class Wallet(models.Model):
    user = models.ForeignKey(user_details,on_delete=models.CASCADE)
    wallet_balance = models.IntegerField(default=0)
    
class Review(models.Model):
    book = models.ForeignKey(books, on_delete=models.CASCADE)
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Review for {self.order_item.book.title} by {self.user.username}"
