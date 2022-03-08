import factory
import datetime

from acc.models import User

class ShopFactory(factory.Factory): 

    class Meta:
        model = User

    email = "yepin58022@toudrum.com"
    full_name = "John Doe"
    date_of_birth = datetime.date.today()
    gender = "male"
    address = "Indore"
    is_active = True
    is_admin = False
    role = "shopowner"
    shopname = "cafe coffee day"
    shopaddress = "Indore"
    shopdesc = "A place to go when you feel like drinking coffee"
    is_staff = False
    password = "shubham@1"

