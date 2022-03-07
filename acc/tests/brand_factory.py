import factory
import datetime

from acc.models import Brand

class BrandFactory(factory.Factory): 

    class Meta:
        model = Brand

    name = "Nescafe"
    

    

