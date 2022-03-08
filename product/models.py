from django.db import models
from sqlite3 import Timestamp
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from acc.models import User

# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=50)

class Brand(models.Model):

    name = models.CharField(max_length=50)

class Product(models.Model):
    """Model for products listed by shops"""
    categories = (
        ("electronics","electronics") , ("footwear","footwear") ,
        ("accesories","accesories")
    )
    price = models.FloatField()
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    provider = models.ForeignKey(User , on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='images/', default=None)
    color = models.CharField(max_length =20 , null=True, blank=True)
    material = models.CharField(max_length=50 , null=True , blank=True)
    

    def __str__(self):
        """returns the name of product"""
        return self.name

    def price_of(self):
        """returns the price of product"""

        return self.price

    def is_available(self , required):
        """check if the product is available"""

        return self.quantity > required
# class rating(models.Model):

#     value = models.IntegerField(
#         default=1,
#         validators=[
#             MaxValueValidator(100),
#             MinValueValidator(1)
#         ]
#     )

#     rated_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     comment = models.TextField(default=None, null=True, blank=True)
# class Category(models.Model):

#     name = models.CharField(max_length=50)

# class Brand(models.Model):

#     name = models.CharField(max_length=50)

# class Product(models.Model):
#     """Model for products listed by shops"""
#     categories = (
#         ("electronics","electronics") , ("footwear","footwear") ,
#         ("accesories","accesories")
#     )
#     price = models.FloatField()
#     name = models.CharField(max_length = 100)
#     description = models.CharField(max_length = 500)
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     provider = models.ForeignKey(User , on_delete=models.CASCADE)
#     image = models.ImageField(upload_to ='images/', default=None)
#     color = models.CharField(max_length =20 , null=True, blank=True)
#     material = models.CharField(max_length=50 , null=True , blank=True)
    

#     def __str__(self):
#         """returns the name of product"""
#         return self.name

#     def price_of(self):
#         """returns the price of product"""

#         return self.price

#     def is_available(self , required):
#         """check if the product is available"""

#         return self.quantity > required
class Rating(models.Model):

    value = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
    )

    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(default=None, null=True, blank=True)

class Wishlist(models.Model):
    """Model to shortlist Products that you like"""

    user = models.OneToOneField(User , on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)

# class Cart(models.Model):
#     """model that contains all items to buy"""

#     user = models.OneToOneField(User , on_delete=models.CASCADE)

# class CartItems(models.Model):
#     """Constitutes entries for cart"""

#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default = 1)
#     cart = models.ForeignKey(Cart , on_delete=models.CASCADE)

# class TimeStamp(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True
# class Order(TimeStamp):
#     """Creates a particular order for a user when he hits buy"""
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     total = models.IntegerField()
#     status = models.CharField(max_length=10)


# class OrderItems(models.Model):
#     """Particular entry for each product"""

#     order = models.ForeignKey(Order,on_delete=models.CASCADE)
#     item = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default = 1)
#     total = models.IntegerField()
#     status = models.CharField(max_length=50, default = 'Waiting for delivery')