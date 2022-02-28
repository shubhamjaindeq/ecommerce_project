"""program logic for the acc app"""
import json
import datetime

from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .filters import ProductFilter
from .models import User, Product, Wishlist, Cart, CartItems, Order, OrderItems
from .forms import RequestResponseForm, ShopSignupForm, AddUserForm,  AddProduct


class IndexView(ListView):
    """Landing page"""

    template_name = 'customer/customerindex.html'

    model = Product

    @method_decorator([login_required])
    def get(self, request ):
        """gets called if the request methods is get"""
        if request.user.role == "customer":
            productlist = Product.objects.all()
            if request.GET.get('search') is not None :
                keyword = request.GET.get('search')
                productlist = productlist.filter(
                    Q(name__icontains=keyword) | Q(description__icontains = keyword )
                )

            if request.GET.get('sortby') == "plth":
                productlist = productlist.order_by('price')
            elif request.GET.get('sortby') == "phtl":
                productlist = productlist.order_by('-price')
            elif request.GET.get('sortby') == "rlth":
                productlist = productlist.order_by('rating')
            else:
                productlist = productlist.order_by('-rating')

            productfilter = ProductFilter(request.GET, queryset=productlist)
            productlist = productfilter.qs
            paginator = Paginator(productlist, 2)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(
                request,self.template_name,
                {'productlist': page_obj, 'productFilter' : productfilter }
            )

        elif request.user.role == "shopowner":
            return render(request,'shop/shopindex.html' )

        return render(request,'adminindex.html' )


class ApprovalView(View):
    """handles rendering and fetching of form for admin to accept and reject
    requests"""

    form_class = RequestResponseForm
    template_name = 'requestresponse.html'

    @method_decorator([login_required])
    def get(self, request, **kwargs):
        """gets called if the request methods is get"""

        if request.user.role != "admin":
            return redirect("/accounts/logout/")
        user_id = kwargs['id']
        request_by = User.objects.get(id=user_id)
        form = self.form_class()
        return render(request , self.template_name , {'form' : form  , 'request_by' : request_by })

    def post(self, request, **kwargs):
        """gets called if the request methods is get"""

        form = self.form_class(request.POST)
        if form.is_valid():
            approval_response = form.cleaned_data['response']
            user_id = kwargs['id']
            request_by = User.objects.get(id=user_id)
            if approval_response == "approve":
                request_by.is_active = True
                request_by.save()

            elif approval_response == "reject":

                request_by.delete()

            return redirect('/')

class UserListView(ListView):
    """admin gets a list of user"""
    template_name = 'userlist.html'
    model = User

class ProductListView(ListView):
    """Shop Owner gets a list of his Products"""
    template_name = 'shop/productlist.html'
    model = Product
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        """extending the default behaviour of list view data"""
        if self.request.user.role != "shopowner":

            return redirect("/accounts/logout")

        products = Product.objects.filter(provider=self.request.user)
        return products

class UserProfileView(DetailView):
    """Handles My profile view for customer"""
    model = User
    template_name = 'customer/profile.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ShopProfileView(DetailView):
    """Handles My profile view for customer"""
    model = User
    template_name = 'shop/profile.html'

class RequestsView(ListView):
    """collect all pending requests and show it to amdin"""
    model = User
    template_name = "requestlist.html"
    context_object_name = 'lst'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        """only show those users who have is_active = False"""
        if self.request.user.role != "admin":
            return redirect("/accounts/logout")

        return User.objects.filter(is_active = False)

class ShopSignupFormView(FormView):
    """Renders and handles form for registration of shop"""
    form_class = ShopSignupForm
    template_name = "account/shopsignup.html"
    success_url ="/accounts/login"

    def form_valid(self, form):

        """verify if the form data is valid and fetch attributes"""
        user = User()
        user.email = form.cleaned_data['email']
        user.password = form.cleaned_data['password2']
        user.set_password(user.password)
        user.role = "shopowner"
        user.shopname = form.cleaned_data['shopname']
        user.shopdesc =form.cleaned_data['shopdesc']
        user.shopaddress = form.cleaned_data['shopaddress']
        user.full_name = form.cleaned_data['full_name']
        user.address = form.cleaned_data['address']
        user.gender = form.cleaned_data['gender']
        user.date_of_birth = form.cleaned_data['date_of_birth']
        user.save()
        return super().form_valid(form)

class AddUserFormView(FormView):
    """Admin can add users by himself"""
    form_class = AddUserForm
    template_name = "adduser.html"
    success_url ="/"

    #@method_decorator(login_required)
    def form_valid(self, form):
        
        """verify if the form data is valid and fetch attributes"""
        if self.request.user.role != "admin":
            return redirect("/accounts/logout")

        print(form.cleaned_data)
        user = User()
        user.email = form.cleaned_data['email']
        user.password = form.cleaned_data['password2']
        user.set_password(form.cleaned_data['password2'])
        user.role = form.cleaned_data['role']
        user.shopname = form.cleaned_data['shopname']
        user.shopdesc =form.cleaned_data['shopdesc']
        user.shopaddress = form.cleaned_data['shopaddress']
        user.full_name = form.cleaned_data['full_name']
        user.address = form.cleaned_data['address']
        user.gender = form.cleaned_data['gender']
        user.date_of_birth = form.cleaned_data['date_of_birth']
        user.save()
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    """Renders and updates customer details"""
    model = User
    template_name = 'customer/editprofile.html'
    fields = [
        "full_name",
        "address",
        "date_of_birth",
        "email",
    ]
    success_url ="/"

class UserUpdateByAdminView(View):

    model = User
    template_name = "updateuserbyadmin.html"

    @method_decorator([login_required])
    def get(self, request , **kwargs):
        """Update User information by admin"""

        if request.user.role != 'admin':
            return redirect("/accounts/logout")

        user_id = kwargs['pk']
        request_by = User.objects.get(id=user_id)
        response_data = {
        'id': request_by.id,
        'full_name': request_by.full_name,
        'email': request_by.email,
        'role' : request_by.role,
        'address' : request_by.address,
    }

        return JsonResponse(response_data)

    def post(self, request):
        data = json.loads(request.POST.get('data', ''))
        obj = data['obj']
        obj_id = obj['id']
        address = obj['address']
        full_name = obj['full_name']
        role = obj['role']
        email = obj['email']
        request_by = User.objects.get(id=obj_id)
        request_by.address = address
        request_by.full_name = full_name
        request_by.role = role
        request_by.email = email
        request_by.save()
        return redirect("/")

class UserDeleteByAdmin(View):
    """view for admin to delete users"""

    def post(self , request):
        """recieved post data from ajax"""

        if request.user.role != "admin":
            return redirect("/accounts/logout")
        data = json.loads(request.POST.get('data', ''))
        user_id = data['obj']['id']
        print(id)
        request_by = User.objects.get(id=user_id)
        request_by.delete()
        return redirect("/listusers")

class ShopUpdateView(UpdateView):
    """Renders and updates shop details"""
    model = User
    template_name = 'shop/editprofile.html'
    fields = [
        "full_name",
        "address",
        "date_of_birth",
        "email",
        "shopname",
        "shopaddress",
        "shopdesc",
    ]
    success_url ="/"

class AddProductFormView(FormView):
    """Add a new product to shop"""

    template_name = 'shop/addproduct.html'
    form_class = AddProduct
    success_url = '/thanks/'

    def form_valid(self, form):
        """checks if the data is valid and then adds the product"""

        if self.request.user.role != "shopowner":
            return redirect("/accounts/logout")
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        product = Product()
        product.name = form.cleaned_data['name']
        product.price = form.cleaned_data['price']
        product.description = form.cleaned_data['description']
        product.image = form.cleaned_data['image']
        product.brand = form.cleaned_data['brand']
        product.category = form.cleaned_data['category']
        product.provider = user
        product.quantity = form.cleaned_data['quantity']
        product.color = form.cleaned_data['color']
        product.material = form.cleaned_data['material']
        product.save()
        return redirect('/')

class ProductUpdateView(View):
    """Update details of a product."""

    model = Product

    def get(self, request, **kwargs):
        """gets called if the request method is get
        and prefills data"""

        if request.user.role != "shopowner":
            return redirect("/accounts/logout")
        print("product update  clalled")
        print(self.kwargs)
        product_id = self.kwargs['pk']
        request_for = Product.objects.get(id=product_id)
        responsedata = {
        'id' : request_for.id,
        'name': request_for.name,
        'price': request_for.price,
        'category' : request_for.category,
        'brand' : request_for.brand,
        'description' : request_for.description,
        'quantity': request_for.quantity,
        'image' : json.dumps(str(request_for.image)),
        'color' : request_for.color,
        'material' : request_for.material
    }
        return JsonResponse(responsedata)

    def post(self, request , **kwargs):
        """gets called if the request method is post and data is updated"""

        if request.user.role != "shopowner":
            return redirect("/accounts/logout")
        data = request.POST
        print(request.FILES['image'])
        name = data['name']
        product_id = kwargs['pk']
        category = data['category']
        quantity = data['quantity']
        color = data['color']
        material = data['material']
        brand = data['brand']
        description = data['description']
        product = Product.objects.get(id=product_id)
        product.category = category
        product.name = name
        product.quantity = quantity
        product.image = request.FILES['image']
        product.color = color
        product.material = material
        product.brand = brand
        product.description = description
        product.save()
        return redirect("/listproducts/")

class ProductDeleteView(View):
    """Deletes a product when requested by owner"""

    def post(self , request):
        """recieved post data from ajax"""

        if request.user.role != "shopowner":
            return redirect("/accounts/logout")
        data = json.loads(request.POST.get('data', ''))
        product_id = data['obj']['id']
        request_by = Product.objects.get(id=product_id)
        request_by.delete()
        return redirect("/listproducts/")

class ProductDetailView(DetailView):
    """Handles My product view for customer"""

    model = Product
    template_name = 'customer/productdetail.html'

class BuyNowView(View):
    """Buy product"""
    def get(self, request, **kwargs):
        """accepts buy requests and check availability"""
        if request.user.role != "customer":
            return redirect("/accounts/logout")

        user = User.objects.get(id=request.user.id)
        order = Order()
        order.user = user
        order.date = datetime.date.today()
        order.status = "pending"
        order.total = 0
        order.save()
        orderitem = OrderItems()
        orderitem.order = order
        orderitem.item = Product.objects.get(id=kwargs['pk'])
        orderitem.quantity = 1
        orderitem.total = Product.objects.get(id=kwargs['pk']).price
        orderitem.save()
        order.total = orderitem.total
        order.status = "paid"
        order.save()
        return redirect("/myorders")
class AddToWishlistView(View):
    """Add items in wishlist"""

    def get(self, request, **kwargs):
        """process get request to add item"""
        if request.user.role != "customer":
            return redirect("/accounts/logout")
        product_id = self.kwargs['pk']
        user_id = request.user.id
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=user_id)
        if hasattr(user, 'wishlist'):
            wishl = user.wishlist
            wishl.items.add(product)
        else:
            wishl = Wishlist(user = user)
            wishl.save()
            wishl.items.add(product)
        wishl.save()
        return redirect('/')

class WishListView(View):
    """View wishlist"""

    def get(self, request, **kwargs):
        """fetches all items in wishlist"""

        if request.user.role != "customer":
            return redirect("/accounts/logout")
        user_id = request.user.id
        user = User.objects.get(id = user_id)
        wishl = user.wishlist
        object_list = wishl.items.all()
        print(user)
        return render(request, 'customer/mywishlist.html' , { 'object_list' : object_list })

class DeleteFromWishListView(View):
    """Remove item from wishlist"""

    def post(self, request,):
        """Processes post ajax request"""

        if request.user.role != "customer":
            return redirect("/accounts/logout")
        data = json.loads(request.POST.get('data', ''))
        product_id = data['obj']['id']
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=request.user.id)
        wishl = user.wishlist
        wishl.items.remove(product)
        return redirect('/mywishlist/' + str(request.user.id) )

class AddToCartView(View):
    """Adds item to cart"""
    def get(self, request, **kwargs):
        """Adds item to cart"""
        if request.user.role != "customer":
            return redirect("/accounts/logout")
        product = Product.objects.get(id = kwargs['pk'])
        user = User.objects.get(id=request.user.id)

        if hasattr(user, 'cart'):

            cart = user.cart
            content_list = cart.cartitems_set.all()
            found = False
            for entry in content_list:
                if entry.product == product:
                    entry.quantity += 1
                    entry.save()
                    found = True
                    break
            if not found:
                entry = CartItems(product = product , quantity = 1 , cart = cart)
                entry.save()

        else:
            cart = Cart(user=user)
            cart.save()
            cartitems = CartItems(product , 1 , cart)
            cartitems.product = product.id
            cartitems.cart = cart.id
            cartitems.save()
        return redirect('/mycart/' + str(user.id))


class CartView(ListView):
    """view for all items in cart"""

    template_name = "customer/mycart.html"

    def get_queryset(self):
        """prepares list view for cart items"""

        if self.request.user.role != "customer":
            return redirect("/accounts/logout")
        print(self.request.user)
        user = self.request.user
        object_list = user.cart.cartitems_set.all()
        return object_list

class DeleteFromCartView(View):
    """Process request to delete item for cart"""

    def post(self,request):
        """Process Post request to delete item for cart"""

        if request.user.role != "customer":
            return redirect("/accounts/logout")
        data = json.loads(request.POST.get('data', ''))
        entry_id = data['obj']['id']
        entry = CartItems.objects.get(id=entry_id)
        entry.delete()
        return redirect('/mycart/' + str(request.user.id) )

class CheckoutView(View):
    """view for customer to checkout and buy items present in his cart"""

    def get(self,request):
        """process request for checkout from cart"""

        user = User.objects.get(id=request.user.id)
        all_items = user.cart.cartitems_set.all()
        total_price = 0
        order = Order()
        order.user = user
        order.date = datetime.date.today()
        order.total = 0
        order.status = "pending"
        order.save()
        for item in all_items:
            product = item.product
            quantity = item.quantity
            total = product.price * quantity
            total_price += total
            provider = item.product.provider
            orderitem = OrderItems(order=order, item = product, quantity=quantity, total=total, provider = provider)
            orderitem.save()

        order.total = total_price
        order.status = "paid"
        order.save()
        for items in all_items:
            items.delete()
        return redirect("/")

class MyOrdersView(ListView):
    """"list view for all orders by a customer"""

    template_name = "customer/myorders.html"
    model = Order

    def get_queryset(self):
        """fetch and prepare data for the view"""

        user = User.objects.get(id=self.request.user.id)
        order_list = Order.objects.filter(user = user)
        return order_list

class CancelOrderView(View):
    """cancel a order"""

    def get(self, *args, **kwargs):
        """change status of order from paid to cancelled"""
        order = Order.objects.get(id = kwargs['pk'])
        order.status = "cancelled"
        order.save()
        return redirect("/myorders")

class OrderDetailView(DetailView):
    """renders detail view for order"""

    model = Order
    template_name = "customer/orderdetail.html"

    def get_context_data(self, **kwargs):
        """prepares data for the order details"""
        context = super().get_context_data(**kwargs)
        order = kwargs['object']
        item_list = OrderItems.objects.filter(order=order)
        context['items_list'] = item_list
        return context

class RemoveItemView(View):
    """remove an item from order"""

    def get(self, *args ,**kwargs):
        """process request for removal of an item"""
        orderitem = OrderItems.objects.get(id = kwargs['pk'])
        order_id = str(orderitem.order.id)
        print(order_id)
        orderitem.delete()
        return redirect("/orderdetail/"+order_id)

class ShopOrderView(ListView):

    template_name = "shop/myorders.html"
    model = Order

    def get_queryset(self):
        """fetch and prepare data for the view"""

        user = User.objects.get(id=self.request.user.id)
        items_list = OrderItems.objects.filter(provider = user)
        print(items_list)
        
        return items_list