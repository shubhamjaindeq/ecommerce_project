import factory
import datetime

from product.models import Category

class CategoryFactory(factory.Factory): 

    class Meta:
        model = Category

    name = "Electronics"
    

    

