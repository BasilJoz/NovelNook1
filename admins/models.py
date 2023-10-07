from django.db import models
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    

    def __str__(self):
        return self.name
    
class books(models.Model):
    title = models.CharField(max_length=200)
    categories = models.ForeignKey(Category,on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    discount_percent = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    deleted = models.BooleanField(default=False)  
    discription = models.TextField()
    
    
    def soft_delete(self):
        self.deleted = True
        self.save()
    
    def undelete(self):
        self.deleted = False
        self.save()
    
    
    
    def __str__(self):
        return self.title
    
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    minimum_amount = models.IntegerField()
    discount = models.DecimalField(max_digits=20, decimal_places=2)
    is_expired = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_to = models.DateField()

    def _str_(self):
        return self.coupon_code
    
    def is_valid(self):
        now = timezone.now().date()
        return self.valid_from <= now <= self.valid_to
    

    