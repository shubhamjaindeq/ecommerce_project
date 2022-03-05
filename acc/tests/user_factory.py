import factory
import datetime

from acc.models import User

class UserFactory(factory.Factory): 

    class Meta:
        model = User

    email = "taviba5898@xindax.com"
    full_name = "John Doe"
    date_of_birth = datetime.date.today()
    gender = "male"
    address = "Indore"
    is_active = True
    is_admin = False
    role = "customer"
    is_staff = False
    password = "shubham@1"

