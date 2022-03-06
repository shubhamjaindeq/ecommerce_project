import factory
import datetime

from acc.models import Product

class ProductFactory(factory.Factory): 

    class Meta:
        model = Product

    price = 100
    description = "Latte coffee with wonderful taste"
    category = "electronics"
    name = "Latte"
    brand = "Nescafe"
    quantity = 100
    soldcount = 0
    image = factory.django.ImageField(color='blue')
    color = "black"
    material = "organic"
    rating = 50


    

