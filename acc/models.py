"""ORM models are defined maps databse to django views"""
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    """manager for user , overrides creation of new users"""

    def create_user(self, full_name=None, date_of_birth=None, email=None, gender=None,
                    address=None, role=None, password=None, is_admin=False, shopname = None, shopdesc = None, shopaddress = None):
        """create customer and shop"""

        if not email:
            raise ValueError('Users must have an email address attached ')
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user.set_password(password)
        user.role = role
        user.full_name= full_name
        user.date_of_birth= date_of_birth
        user.gender= gender
        user.address= address
        user.is_active = True
        user.is_staff = False
        user.set_password(password)
        user.shopname = shopname
        user.shopaddress = shopaddress
        user.shopdesc = shopdesc
        user.save()
        return user

    def create_superuser(
                        self,  full_name=None, date_of_birth=None,
                        shopname=None,shopaddress=None,role = "admin", shopdesc=None, email=None,
                        gender=None,address=None,
                        password=None
        ):
        """creates admin"""
        user = self.create_user(
            email=email,
            password=password,
            full_name=full_name,
            gender=gender,
            address=address,
            date_of_birth=date_of_birth,
            role = role,
        )
        user.shopname = shopname
        user.shopaddress = shopaddress
        user.shopdesc = shopdesc
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser):
    """Customer , Shop and admin model"""
    genderchoices = [
        ("M", "Male"),
        ("F", "Female")
    ]
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    full_name = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=genderchoices, null=True)
    address = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=10, default="customer")
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    shopaddress = models.CharField(null=True, blank=True, max_length=200)
    shopname = models.CharField(null=True, blank=True, max_length=50)
    shopdesc = models.CharField(null=True, blank=True, max_length=500)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """return unique email of that user"""
        if self.role == "shopowner":
            return self.shopname
        return self.email

    def has_perm(self, obj=None):
        """checks if the user has permission to access"""
        print(self,obj)
        return True

    def has_module_perms(self, app_label):
        """checks if the user has permission to access"""
        print(self)
        return True

    @property
    def is_staff_user(self):
        """checks if the user is a staff member"""
        return self.is_admin


class Product(models.Model):
    """Model for products listed by shops"""
    categories = (
        ("electronics","electronics") , ("footwear","footwear") ,
        ("accesories","accesories")
    )
    price = models.FloatField()
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    brand = models.CharField(max_length =50)
    category = models.CharField(choices = categories , max_length = 50)
    quantity = models.IntegerField()
    soldcount = models.IntegerField(default=0)
    provider = models.ForeignKey(User , on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='images/', default=None)
    color = models.CharField(max_length =20 , null=True, blank=True)
    material = models.CharField(max_length=50 , null=True , blank=True)
    rating = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
    )

    def __str__(self):
        """returns the name of product"""
        return self.name

    def price_of(self):
        """returns the price of product"""

        return self.price

    def is_available(self , required):
        """check if the product is available"""

        return self.quantity > required

class Wishlist(models.Model):
    """Model to shortlist Products that you like"""

    user = models.OneToOneField(User , on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)

class Cart(models.Model):
    """model that contains all items to buy"""

    user = models.OneToOneField(User , on_delete=models.CASCADE)

class CartItems(models.Model):
    """Constitutes entries for cart"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)

class Order(models.Model):
    """Creates a particular order for a user when he hits buy"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField()
    status = models.CharField(max_length=10)


class OrderItems(models.Model):
    """Particular entry for each product"""

    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    total = models.IntegerField()
    provider = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=50, default = 'Waiting for delivery')
