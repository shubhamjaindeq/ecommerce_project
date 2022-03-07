import json
import factory
import datetime
import base64               # for decoding base64 image
import tempfile             # for setting up tempdir for media
from io import BytesIO 
from urllib import response

from django.core import mail
from django.db.models import F
from django.test import TestCase, Client
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from allauth.account.admin import EmailAddress

from acc.forms import AddProduct, RequestResponseForm
from acc.views import AddProductFormView
from . import user_factory, shop_factory, product_factory
from acc.models import User, Product, Wishlist, CartItems, Cart, Order, OrderItems

class CustomerIndexViewsTest(TestCase): 
    """test index page functioning for customer"""
    def setUp(self):
        """data preparation for test"""
        self.client = Client()
        self.email= "taviba5898@xindax.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"
        self.verifyurl = "/accounts/confirm-email/MQ:1nPjV9:M8uIY2IvL3yFqt2XcCoYQkQx3j7vlF2ZhGuS2wCUDsE/"

    def test_landing_without_login(self):
        """test to check if the app redirects to login when user isnt logged in"""
        redirection = self.client.get("/")
        self.assertTemplateNotUsed(redirection, template_name="customer/customerindex.html")
        self.assertRedirects(redirection, "/accounts/login/?next=/")
    
    def test_landing(self):
        """tests login for an authenticated user"""
        user = user_factory.UserFactory.create()
        user.set_password("shubham@1")
        user.save()
        self.client.login(email = self.email, password = self.password1)
        landing = self.client.get("/")
        self.assertTemplateUsed(landing, template_name="customer/customerindex.html")

    def test_search_and_filter_landing(self):
        """test index page with search """
        shop = shop_factory.ShopFactory.create()
        shop.set_password("shubham@1")
        shop.save()
        product = product_factory.ProductFactory.create()
        product.provider = shop
        product.save()
        product = product_factory.ProductFactory.create(category = "accesories")
        product.provider = shop
        product.save()
        user = user_factory.UserFactory.create()
        user.set_password("shubham@1")
        user.save()
        self.client.login(email=user.email, password= self.password1)
        response = self.client.get("/", { "sortby": "rhtl", "search": "latte" })
        self.assertQuerysetEqual(Product.objects.filter(name__icontains= "latte").order_by("rating"),  response.context['products'])
        response = self.client.get("/", { "category": "accesories", })
        self.assertQuerysetEqual(Product.objects.filter(category="accesories"),  response.context['products'])

class CustomerProfileViewsTest(TestCase): 
    """test index page functioning for customer"""
    def setUp(self):
        """data preparation for test"""
        self.client = Client()
        self.email= "taviba5898@xindax.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"
        self.verifyurl = "/accounts/confirm-email/MQ:1nPjV9:M8uIY2IvL3yFqt2XcCoYQkQx3j7vlF2ZhGuS2wCUDsE/"


    def test_profile_view(self):
        """test My profile section for customer"""
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        response = self.client.get("/userprofile/{}".format(user.id))
        self.assertEqual(response.context['object'], user)
        self.assertTemplateUsed(response , template_name="customer/profile.html")

    def test_edit_profile_view(self):
        """test edit profile for customer"""
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        response = self.client.get("/edituserdetails/{}".format(user.id))
        self.assertTemplateUsed(response, template_name="customer/editprofile.html")
        response = self.client.post("/edituserdetails/{}".format(user.id), {
            "full_name": "shubham jain", 
            "email": self.email,
            "address": self.address,
            "date_of_birth" : "2022-01-01"
            }
        ) 
        self.assertEqual(User.objects.get(email = self.email).full_name, "shubham jain")
        self.assertEqual("/", response.url)

class CustomerProductView(TestCase):
    """tests for customers interaction with products"""
    def setUp(self):
        """data preparation for test"""
        self.client = Client()
        self.email= "taviba5898@xindax.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"
        self.verifyurl = "/accounts/confirm-email/MQ:1nPjV9:M8uIY2IvL3yFqt2XcCoYQkQx3j7vlF2ZhGuS2wCUDsE/"

    def test_product_details(self):
        """tests product details request for customer"""
        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()

        response = self.client.get("/productdetail/{}".format(product.id))
        self.assertTemplateUsed(response, template_name="customer/productdetail.html")
        self.assertEqual(product, response.context['product'])

    def test_add_to_empty_wishlist(self):
        """test to check if wishlist is being created and add the first product"""

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        response = self.client.get("/addtowishlist/{}".format(product.id))
        self.assertEqual(response.url, "/")
        wishlist = Wishlist.objects.get(user = user)
        self.assertEqual(wishlist.items.all()[0], product)

    def test_add_to_existing_wishlist(self):
        """test to check if wishlist is being created and add the first product"""

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        self.client.get("/addtowishlist/{}".format(product.id))
        product = product_factory.ProductFactory.create(name = "cappucino")
        product.provider = shop
        product.save()
        self.client.get("/addtowishlist/{}".format(product.id))
        wishlist = Wishlist.objects.get(user=user)
        self.assertEqual(len(wishlist.items.all()), 2)

    def test_my_wishlist_view(self):
        """test My wish wishlist view for customers."""

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        self.client.get("/addtowishlist/{}".format(product.id))
        product = product_factory.ProductFactory.create(name = "cappucino")
        product.provider = shop
        product.save()
        self.client.get("/addtowishlist/{}".format(product.id))
        response = self.client.get("/mywishlist/{}".format(user.id))
        #self.assertEqual(Wishlist.objects.get(user = user).items.all(), response.context['object_list'])
        self.assertTemplateUsed(response, template_name="customer/mywishlist.html")

    def test_delete_from_wishlist(self):
        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        self.client.get("/addtowishlist/{}".format(product.id))   
        response = self.client.post("/deletefromwishlist/",{'data': ['{"obj":{"id":"1","data":{"content":"xxx"}}}']}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        redirected_to = self.client.get(response.url)
        self.assertTemplateUsed(redirected_to, template_name="customer/mywishlist.html")
        self.assertEqual(len(Wishlist.objects.get(user = user).items.all()), 0)

    def test_add_to_cart_first_time(self):
        """test to check if cart is createtd and items are added"""
        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        self.assertEqual(len(Cart.objects.filter(user=user)), 0)
        response = self.client.get("/addtocart/{}".format(product.id))
        self.assertEqual(response.url, "/mycart/{}".format(user.id))
        self.assertEqual(len(Cart.objects.get(user=user).cartitems_set.all()), 1)

    def test_addtocart_with_existing_cart(self):
        """test to add item to an exixting cart"""
        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        response = self.client.get("/addtocart/{}".format(product.id))
        self.assertEqual(len(Cart.objects.get(user=user).cartitems_set.all()), 1)
        product = product_factory.ProductFactory.create(name = "Espresso")
        product.provider = shop
        product.save()
        response = self.client.get("/addtocart/{}".format(product.id))
        self.assertEqual(len(Cart.objects.get(user=user).cartitems_set.all()), 2)

    def test_cart_view(self):
        """test to fetch all items in our cart"""

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        response = self.client.get("/mycart/{}".format(user.id))
        self.assertTemplateUsed(response, template_name="customer/mycart.html")

    def test_delete_from_cart_view(self):
        """test to delete items from cart view"""

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        self.client.get("/addtocart/{}".format(product.id))
        self.assertEqual(len(Cart.objects.get(user=user).cartitems_set.all()), 1)
        self.client.post("/deletefromcart/", {'data': ['{"obj":{"id":"1","data":{"content":"xxx"}}}']},  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(Cart.objects.get(user=user).cartitems_set.all()), 0)

class CustomerBuyView(TestCase):

    def setUp(self):
        """data preparation for test"""
        self.client = Client()
        self.email= "taviba5898@xindax.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"

    def test_checkout_from_cart(self):

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        price = product.price
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        self.client.get("/addtocart/{}".format(product.id))
        product = product_factory.ProductFactory.create(name = "Espresso")
        product.provider = shop
        product.save()
        secondprice = product.price

        self.client.get("/addtocart/{}".format(product.id))
        response = self.client.get("/checkout/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Cart.objects.filter(user=user)[0].cartitems_set.all()), 0)
        self.assertEqual(Order.objects.filter(user=user)[0].total, price+secondprice)

    def test_buy_now(self):
        """test to check is customer can directly buy a single product without adding it to the cart"""
        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        price = product.price
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        self.assertEqual(len(Order.objects.filter(user=user)), 0)
        response = self.client.get("/buynow/{}".format(product.id))
        self.assertEqual(len(Order.objects.filter(user=user)), 1)

            
        
class CustomerOrdersTest(TestCase):

    def setUp(self):
        """data preparation for test"""
        self.client = Client()
        self.email= "taviba5898@xindax.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"

    def test_my_orders_view(self):
        """test to fetch orders by customer"""

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        price = product.price
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        self.client.get("/buynow/{}".format(product.id))
        response = self.client.get("/myorders/")
        self.assertTemplateUsed(response, template_name="customer/myorders.html")
        self.assertQuerysetEqual(response.context['object_list'], Order.objects.filter(user=user), ordered = False)

    def test_cancel_order_view(self):
        """test to cancel an order"""

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        price = product.price
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        self.client.get("/buynow/{}".format(product.id))
        order = Order.objects.filter(user=user)[0]
        self.assertEquals(order.status, "paid")
        response = self.client.get("/cancelorder/{}".format(order.id))
        self.assertRedirects(response, "/myorders/")
        self.assertEquals(Order.objects.get(id=order.id).status, "cancelled")

    def test_detail_order_view(self):
        """test to cancel an order"""

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        price = product.price
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        self.client.get("/buynow/{}".format(product.id))
        order = Order.objects.filter(user=user)[0]
        response = self.client.get("/orderdetail/{}".format(order.id))
        self.assertTemplateUsed(response, template_name="customer/orderdetail.html")
        self.assertQuerysetEqual(response.context['items_list'], OrderItems.objects.filter(order=order), ordered= False)
        
    def test_delete_order_tems(self):
        """test to check deletion of an item from order"""

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        price = product.price
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = self.email, password = self.password1)
        self.client.get("/buynow/{}".format(product.id))
        order = Order.objects.filter(user=user)[0]
        item = order.orderitems_set.all()[0]
        response = self.client.get("/removeitem/{}".format(item.id))
        self.assertRedirects(response, "/orderdetail/{}".format(order.id))
        self.assertEqual(len(Order.objects.get(id=order.id).orderitems_set.all()), 0)

class ShopIndexViewsTest(TestCase): 
    """test index page functioning for customer"""
    def setUp(self):
        """data preparation for test"""
        self.client = Client()
        self.shopname = "CCD"
        self.shopaddress = "Indore"
        self.shopdescription = "A place for all your coffee needs"
        self.email= "yepin58022@toudrum.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"
        self.verifyurl = "/accounts/confirm-email/MQ:1nPjV9:M8uIY2IvL3yFqt2XcCoYQkQx3j7vlF2ZhGuS2wCUDsE/"

    def test_landing_without_login(self):
        """test to check if the app redirects to login when user isnt logged in"""
        redirection = self.client.get("/")
        self.assertTemplateNotUsed(redirection, template_name="shop/shopindex.html")
        self.assertRedirects(redirection, "/accounts/login/?next=/")
    
    def test_landing(self):
        """tests login for an authenticated user"""
        shop = shop_factory.ShopFactory.create()
        shop.set_password("shubham@1")
        shop.save()
        self.client.login(email = self.email, password = self.password1)
        landing = self.client.get("/")
        self.assertTemplateUsed(landing, template_name="shop/shopindex.html")

class ShopProfileViewsTest(TestCase): 
    """test index page functioning for customer"""
    def setUp(self):
        """data preparation for test"""
        self.client = Client()
        self.shopname = "CCD"
        self.shopaddress = "Indore"
        self.shopdescription = "A place for all your coffee needs"
        self.email= "yepin58022@toudrum.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"
        self.verifyurl = "/accounts/confirm-email/MQ:1nPjV9:M8uIY2IvL3yFqt2XcCoYQkQx3j7vlF2ZhGuS2wCUDsE/"


    def test_profile_view(self):
        """test My profile section for shop"""
        shop = shop_factory.ShopFactory.create()
        shop.set_password(self.password1)
        shop.save()
        self.client.login(email = self.email, password = self.password1)
        response = self.client.get("/shopprofile/{}".format(shop.id))
        self.assertEqual(response.context['object'], shop)
        self.assertTemplateUsed(response , template_name="shop/profile.html")
        
    def test_edit_profile_view(self):
        """test edit profile for shop"""
        shop = shop_factory.ShopFactory.create()
        shop.set_password(self.password1)
        shop.save()
        self.client.login(email = self.email, password = self.password1)
        response = self.client.get("/editshopdetails/{}".format(shop.id))
        self.assertTemplateUsed(response, template_name="shop/editprofile.html")
        self.assertEqual(shop.shopdesc, "A place to go when you feel like drinking coffee")
        response = self.client.post("/editshopdetails/{}".format(shop.id), {
            "full_name": "shubham jain", 
            "email": self.email,
            "address": self.address,
            "date_of_birth" : "2022-01-01",
            "shopdesc": "A place to chill and drink coffe",
            "shopname": "CCD",
            "shopaddress": "Indore"
            }
        ) 
        self.assertEqual(User.objects.get(email = self.email).shopdesc, "A place to chill and drink coffe")
        self.assertEqual("/", response.url)
TEST_IMAGE = '''
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
'''.strip()                       
class ShopProductTest(TestCase):

    def setUp(self):
        """data preparation for test"""
        self.client = Client()
        self.shopname = "CCD"
        self.shopaddress = "Indore"
        self.shopdescription = "A place for all your coffee needs"
        self.email= "yepin58022@toudrum.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"
        self.verifyurl = "/accounts/confirm-email/MQ:1nPjV9:M8uIY2IvL3yFqt2XcCoYQkQx3j7vlF2ZhGuS2wCUDsE/"

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_add_product(self):
        """test to add product by shop"""
        shop = shop_factory.ShopFactory.create()
        shop.set_password(self.password1)
        shop.save()
        self.client.login(email = self.email, password = self.password1)

                                       # StringIO and BytesIO are parts of io module in python3
        image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),            # use io.BytesIO
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        form = AddProduct(
            {
                "name" : "BATA",
                "price" : 100,
                "quantity" : 20, 
                "brand" : "BATA",
                "category" : "footwear",
                "description": "Nice comfy shoes" ,
                "color": "white",
                "material": "Leather",
                #"image": image
            },
            files={"image": image}
        )
        form.is_valid()
        response = self.client.get("/")
        self.request = response.wsgi_request
        AddProductFormView.form_valid(self ,form)
        self.assertEqual(Product.objects.get(name="BATA").provider, shop)
        response = self.client.get("/addproduct/")
        self.assertTemplateUsed(response, template_name="shop/shopindex.html")

    def test_product_list(self):
        """test My products for shoplist"""
        shop = shop_factory.ShopFactory.create()
        shop.set_password(self.password1)
        shop.save()
        self.client.login(email = self.email, password = self.password1)
        product = product_factory.ProductFactory.create()
        product.provider = shop
        product.save()
        product = product_factory.ProductFactory.create(name= "Shirt")
        product.provider = shop
        product.save()
        response = self.client.get("/listproducts/")
        self.assertTemplateUsed(response, template_name="shop/productlist.html")
        self.assertQuerysetEqual(response.context['object_list'], Product.objects.filter(provider=shop), ordered = False)


    def test_product_update_view(self):
        """test update details of product"""

        shop = shop_factory.ShopFactory.create()
        shop.set_password(self.password1)
        shop.save()
        self.client.login(email = self.email, password = self.password1)
        product = product_factory.ProductFactory.create()
        product.provider = shop
        product.save()
        self.assertEqual(Product.objects.get(id=product.id).price, 100)
        response = self.client.get("/productupdate/{}".format(product.id))
        self.assertEqual(json.loads(response.content)['name'], product.name)
        response = self.client.post("/productupdate/{}".format(product.id), {
            "id": product.id,
            "name" : product.name,
            "price": 10000,
            "brand": product.brand,
            "color": product.color,
            "category": product.category,
            "description": product.description,
            "image": product.image,
            "material": product.material,
            "quantity": product.quantity,
            }
            )
        self.assertRedirects(response, "/listproducts/")
        self.assertEqual(Product.objects.get(id=product.id).price, 10000)
        




    def test_delete_product(self):
        shop = shop_factory.ShopFactory.create()
        shop.set_password(self.password1)
        shop.save()
        self.client.login(email = self.email, password = self.password1)
        product = product_factory.ProductFactory.create()
        product.provider = shop
        product.save()
        self.assertEqual(Product.objects.get(id=product.id), product)
        response = self.client.post("/deleteproduct/",{'data': ['{"obj":{"id":"1","data":{"content":"xxx"}}}']}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(len(Product.objects.filter(id=product.id)), 0)

class ShopOrderTest(TestCase):

    def setUp(self):
        """data preparation for test"""

        self.client = Client()
        self.shopname = "CCD"
        self.shopaddress = "Indore"
        self.shopdescription = "A place for all your coffee needs"
        self.email= "yepin58022@toudrum.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"

    def test_order_list_view(self):
        """test to get a list of all orders for a shop"""

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.set_password(self.password1)
        shop.save()
        product.provider = shop
        product.save()
        user = user_factory.UserFactory.create(email = "taviba5898@xindax.com")
        user.set_password(self.password1)
        user.save()
        self.client.login(email = "taviba5898@xindax.com", password = self.password1)
        self.client.get("/buynow/{}".format(product.id))
        self.client.logout()
        c = self.client.login(email = shop.email, password = "shubham@1")
        response = self.client.get("/shoporder/")
        self.assertQuerysetEqual(response.context['object_list'], OrderItems.objects.filter(provider = shop), ordered = False)

    def test_order_status_update_view(self):
        """test status update for a order item by shop"""
        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.set_password(self.password1)
        shop.save()
        product.provider = shop
        product.save()
        user = user_factory.UserFactory.create(email = "taviba5898@xindax.com")
        user.set_password(self.password1)
        user.save()
        self.client.login(email = "taviba5898@xindax.com", password = self.password1)
        self.client.get("/buynow/{}".format(product.id))
        self.client.logout()
        self.client.login(email = shop.email, password = "shubham@1")
        response = self.client.get("/itemstatusupdate/{}".format(1), {"id": 1})
        self.assertEqual(json.loads(response.content)['status'], "Waiting for delivery")
        response = self.client.post("/itemstatusupdate/{}".format(1), {"id": 1, "status": "Sent Out"})
        self.assertRedirects(response, "/listproducts/")
        self.assertEqual(OrderItems.objects.get(provider = shop).status , "Sent Out")

    def test_sales_report_view(self):
        """test to fetch sales report of products by shop"""

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.set_password(self.password1)
        shop.save()
        product.provider = shop
        product.save()
        user = user_factory.UserFactory.create(email = "taviba5898@xindax.com")
        user.set_password(self.password1)
        user.save()
        self.client.login(email = "taviba5898@xindax.com", password = self.password1)
        self.client.get("/buynow/{}".format(product.id))
        self.client.logout()
        self.client.login(email = shop.email, password = "shubham@1")
        response = self.client.get("/salesreport/")
        self.assertTemplateUsed(response, template_name="shop/salesreport.html")
        products = Product.objects.annotate(
            percentsale = F("soldcount") * 100 / F("quantity")
        ).filter(provider = shop)
        self.assertQuerysetEqual(response.context['productlist'], products, ordered=False)

class AdminIndexTest(TestCase):

    def setUp(self):
        """data preparation for test"""

        self.client = Client()
        self.email= "shujain@deqode.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"

    def test_landing_view(self):

        admin = User.objects.create_superuser(email =  self.email, password = self.password1)
        self.client.login(email = self.email, password = self.password2)
        response = self.client.get("/")
        self.assertTemplateUsed(response, template_name = "adminindex.html")
    
class ApprovalTest(TestCase):

    def setUp(self):
        """data preparation for test"""

        self.client = Client()
        self.email= "shujain@deqode.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"

    def test_approval_list_view(self):

        User.objects.create_superuser(email =  self.email, password = self.password1)
        self.client.post("/signupasshop/", data={
            'email': "yepin58022@toudrum.com",
            'full_name': self.full_name,
            'address': self.address,
            "date_of_birth_month": self.date_of_birth_month,
            "date_of_birth_day": self.date_of_birth_day,
            "date_of_birth_year": self.date_of_birth_year,
            "gender": self.gender,
            'password1': self.password1,
            'password2': self.password2,
            "next" : "/",
            "shopname" : "BATA",
            "shopaddress" : "Indore",
            "shopdesc": "Shoe Shop",
        })
        self.client.post("/accounts/login/", data = {
            'login': "yepin58022@toudrum.com",
            'password': self.password1,
        } )
        self.client.post("/accounts/confirm-email/MQ:1nQ1ZE:9WU3BqNn6oVaPzVQKBfX8LmqsnBZ9pO1K9lsr18tbGQ/", data={})
        self.assertFalse(User.objects.get(email = "yepin58022@toudrum.com").is_active)
        self.client.login(email = self.email, password = self.password1)
        response = self.client.get("/requests/")
        self.assertTemplateUsed(response, template_name="requestlist.html")
        self.assertQuerysetEqual(response.context['object_list'], User.objects.filter(is_active = False), ordered = False)
        
    def test_approval_accept_view(self):
        """test to check id admin can approve or reject a request succesffully"""

        User.objects.create_superuser(email =  self.email, password = self.password1)
        self.client.post("/signupasshop/", data={
            'email': "yepin58022@toudrum.com",
            'full_name': self.full_name,
            'address': self.address,
            "date_of_birth_month": self.date_of_birth_month,
            "date_of_birth_day": self.date_of_birth_day,
            "date_of_birth_year": self.date_of_birth_year,
            "gender": self.gender,
            'password1': self.password1,
            'password2': self.password2,
            "next" : "/",
            "shopname" : "BATA",
            "shopaddress" : "Indore",
            "shopdesc": "Shoe Shop",
        })
        self.client.post("/accounts/login/", data = {
            'login': "yepin58022@toudrum.com",
            'password': self.password1,
        } )
        self.client.post("/accounts/confirm-email/MQ:1nQ1ZE:9WU3BqNn6oVaPzVQKBfX8LmqsnBZ9pO1K9lsr18tbGQ/", data={})
        mail_to_admin = mail.outbox[1].body
        self.client.login(email = self.email, password = self.password1)
        response = self.client.get(mail_to_admin)
        self.assertTemplateUsed(response, template_name="requestresponse.html")
        self.assertEqual(response.context['request_by'], User.objects.get(email = "yepin58022@toudrum.com" ))
        response = self.client.get("/")
        self.request = response.wsgi_request
        redirect_to = self.client.post("/approval/{}".format(2), {"response": "approve", "message": "approved"})
        self.assertRedirects(redirect_to, "/")
        self.assertTrue(User.objects.get(email = "yepin58022@toudrum.com").is_active)

    def test_approval_reject_view(self):
        """test to check id admin can approve or reject a request succesffully"""

        User.objects.create_superuser(email =  self.email, password = self.password1)
        self.client.post("/signupasshop/", data={
            'email': "yepin58022@toudrum.com",
            'full_name': self.full_name,
            'address': self.address,
            "date_of_birth_month": self.date_of_birth_month,
            "date_of_birth_day": self.date_of_birth_day,
            "date_of_birth_year": self.date_of_birth_year,
            "gender": self.gender,
            'password1': self.password1,
            'password2': self.password2,
            "next" : "/",
            "shopname" : "BATA",
            "shopaddress" : "Indore",
            "shopdesc": "Shoe Shop",
        })
        self.client.post("/accounts/login/", data = {
            'login': "yepin58022@toudrum.com",
            'password': self.password1,
        } )
        self.client.post("/accounts/confirm-email/MQ:1nQ1ZE:9WU3BqNn6oVaPzVQKBfX8LmqsnBZ9pO1K9lsr18tbGQ/", data={})
        mail_to_admin = mail.outbox[1].body
        self.client.login(email = self.email, password = self.password1)
        response = self.client.get(mail_to_admin)
        self.assertTemplateUsed(response, template_name="requestresponse.html")
        self.assertEqual(response.context['request_by'], User.objects.get(email = "yepin58022@toudrum.com" ))
        response = self.client.get("/")
        self.request = response.wsgi_request
        redirect_to = self.client.post("/approval/{}".format(2), {"response": "reject", "message": "approved"})
        self.assertRedirects(redirect_to, "/")
        self.assertEqual(len(User.objects.filter(email = "yepin58022@toudrum.com")), 0)

class ManageUserTest(TestCase):

    def setUp(self):
        """data preparation for test"""

        self.client = Client()
        self.email= "shujain@deqode.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"

    def test_list_users(self):

        user = user_factory.UserFactory.create(email = "taviba5898@xindax.com")
        user.set_password(self.password1)
        user.save()
        User.objects.create_superuser(email =  self.email, password = self.password1)
        self.client.login(email = self.email, password = self.password1)
        response = self.client.get("/listusers/")
        self.assertTemplateUsed(response, template_name = "userlist.html")
        self.assertQuerysetEqual(response.context['object_list'], User.objects.all(), ordered = False)

    def test_add_shop(self):

        data = { "email": "yepin58022@toudrum.com" ,
                "full_name": "Dalton Tillman",
                "address": "Esse excepturi illum do rerum minus nemo",
                "date_of_birth_month": 5,
                "date_of_birth_day": 21,
                "date_of_birth_year": 2023,
                "gender": "F",
                "shopname": "Elmo Byers",
                "shopaddress": "Placeat et perferendis laborum ex accusamus aliquid dolor commodo ab aliqua Consequatur nostrum tenetur possimus aut at enim",
                "shopdesc": "Consectetur labore eum dolore nobis voluptas in nesciunt quia proident illum laboriosam",
                "role": "shopowner",
                "password1": "shubham@1",
                "password2": "shubham@1"

        }
        
        User.objects.create_superuser(email =  self.email, password = self.password1)
        self.client.login(email = self.email, password = self.password1)
        self.assertEqual(len(User.objects.filter(email = "yepin58022@toudrum.com")), 0)
        response = self.client.post("/adduser/", data)
        self.assertRedirects(response, "/")
        self.assertEqual(len(User.objects.filter(email = "yepin58022@toudrum.com")), 1)

    def test_user_orders_by_admin(self):
        shop = shop_factory.ShopFactory.create()
        shop.set_password(self.password1)
        shop.save()
        user = user_factory.UserFactory.create()
        User.objects.create_superuser(email =  self.email, password = self.password1)
        self.client.login(email = self.email, password = self.password1)
        self.assertEqual(User.objects.get(id=shop.id).full_name, "John Doe")
        response = self.client.get("/userupdatebyadmin/{}".format(1))
        self.assertEqual(json.loads(response.content)['full_name'], shop.full_name)
        response = self.client.post("/userupdatebyadmin/",{'data': ['{"obj":{"address":"Bhopal", "full_name":"Shubham Jain","role":"shopowner","email":"yepin58022@toudrum.com", "id":"1" ,"data":{"content":"xxx"}}}']}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertRedirects(response, "/")
        self.assertEqual(User.objects.get(email= "yepin58022@toudrum.com").full_name, "Shubham Jain")

    def test_user_delete_by_admin(self):
        shop = shop_factory.ShopFactory.create()
        shop.set_password(self.password1)
        shop.save()
        User.objects.create_superuser(email =  self.email, password = self.password1)
        self.client.login(email = self.email, password = self.password1)
        response = self.client.post("/userdeletebyadmin/",{'data': ['{"obj":{"id":"1" ,"data":{"content":"xxx"}}}']}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.url, "/listusers")
        self.assertEqual(len(User.objects.filter(email= "yepin58022@toudrum.com")), 0)

class ManageOrdersandProductsTest(TestCase):

    def setUp(self):
        """data preparation for test"""

        self.client = Client()
        self.email= "shujain@deqode.com"
        self.full_name = "shubham jain"
        self.address = "indore"
        self.date_of_birth_month = 8
        self.date_of_birth_day = 8
        self.date_of_birth_year =  2027
        self.gender = "M"
        self.password1 = "shubham@1"
        self.password2 = "shubham@1"

    def test_user_order_view(self):

        product = product_factory.ProductFactory.create()
        shop = shop_factory.ShopFactory.create()
        shop.save()
        product.provider = shop
        product.save()
        price = product.price
        user = user_factory.UserFactory.create()
        user.set_password(self.password1)
        user.save()
        self.client.login(email = "taviba5898@xindax.com", password = self.password1)
        self.client.get("/buynow/{}".format(product.id))
        User.objects.create_superuser(email =  self.email, password = self.password1)
        self.client.login(email = self.email, password = self.password1)
        response = self.client.get("/userorders")
        self.assertTemplateUsed(response, template_name="userorders.html")
        self.assertQuerysetEqual(response.context['orderlist'], Order.objects.all(), ordered = False)

        

        





