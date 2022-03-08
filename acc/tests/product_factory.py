import factory
import datetime

from product.models import Product

class ProductFactory(factory.Factory): 

    class Meta:
        model = Product

    price = 100
    description = "Latte coffee with wonderful taste"
    name = "Latte"
    quantity = 100
    image = factory.django.ImageField(color='blue')
    color = "black"
    material = "organic"
    rating = 50


    

