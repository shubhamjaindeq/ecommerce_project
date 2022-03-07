import factory
import datetime

from acc.models import Category

class CategoryFactory(factory.Factory): 

    class Meta:
        model = Category

    name = "Electronics"
    

    

