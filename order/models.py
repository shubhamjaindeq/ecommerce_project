from django.db import models
from acc.models import User
from product.models import Product

# Create your models here.
class Cart(models.Model):
    """model that contains all items to buy"""

    user = models.OneToOneField(User , on_delete=models.CASCADE)

class CartItems(models.Model):
    """Constitutes entries for cart"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class Order(TimeStamp):
    """Creates a particular order for a user when he hits buy"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField()
    status = models.CharField(max_length=10)


class OrderItems(models.Model):
    """Particular entry for each product"""

    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    total = models.IntegerField()
    status = models.CharField(max_length=50, default = 'Waiting for delivery')