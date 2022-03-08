import factory
import datetime

from product.models import Brand

class BrandFactory(factory.Factory): 

    class Meta:
        model = Brand

    name = "Nescafe"
    

    

