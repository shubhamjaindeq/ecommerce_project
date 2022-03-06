import datetime

from django.core import mail
from django.test import TestCase, Client

from allauth.account.admin import EmailAddress

from acc.models import User, Product, Wishlist, CartItems, Cart, Order, OrderItems
from . import user_factory, shop_factory, product_factory

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
