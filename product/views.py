import json
from django.shortcuts import render
from django.http import JsonResponse
from product.models import Product, Wishlist, Brand,Category
from order.models import Cart , CartItems
from acc.models import User
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from product.forms import AddProduct
# Create your views here.


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

    def get_context_data(self, **kwargs):
        """prepares data for the product details"""
        product = kwargs['object']
        product.percentsale = product.quantity * product.quantity / 100
        context = super().get_context_data(**kwargs)
        context['product'] = product
        return context
    
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
        return redirect('/dashboard')

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
        return redirect('/product/mywishlist/' + str(request.user.id) )

# class AddToCartView(View):
#     """Adds item to cart"""
#     def get(self, request, **kwargs):
#         """Adds item to cart"""
#         if request.user.role != "customer":
#             return redirect("/accounts/logout")
#         product = Product.objects.get(id = kwargs['pk'])
#         user = User.objects.get(id=request.user.id)

#         if hasattr(user, 'cart'):

#             cart = user.cart
#             content_list = cart.cartitems_set.all()
#             found = False
#             for entry in content_list:
#                 if entry.product == product:
#                     entry.quantity += 1
#                     entry.save()
#                     found = True
#                     break
#             if not found:
#                 entry = CartItems(product = product , quantity = 1 , cart = cart)
#                 entry.save()

#         else:
#             cart = Cart(user=user)
#             cart.save()
#             cartitems = CartItems(quantity = 1)
#             cartitems.product = product
#             cartitems.cart = cart
#             cartitems.save()
#         return redirect('/product/mycart/' + str(user.id))


# class CartView(ListView):
#     """view for all items in cart"""

#     template_name = "customer/mycart.html"

#     def get_queryset(self):
#         """prepares list view for cart items"""

#         if self.request.user.role != "customer":
#             return redirect("/accounts/logout")
#         user = self.request.user
#         if not hasattr(user, 'cart'):
#             return redirect("/")
#         object_list = user.cart.cartitems_set.all()
#         return object_list

# class DeleteFromCartView(View):
#     """Process request to delete item for cart"""

#     def post(self,request):
#         """Process Post request to delete item for cart"""

#         if request.user.role != "customer":
#             return redirect("/accounts/logout")
#         data = json.loads(request.POST.get('data', ''))
#         entry_id = data['obj']['id']
#         entry = CartItems.objects.get(id=entry_id)
#         entry.delete()
#         return redirect('/mycart/' + str(request.user.id) )

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

class AddProductFormView(FormView):
    """Add a new product to shop"""

    template_name = 'shop/addproduct.html'
    form_class = AddProduct
    success_url = '/'

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
        category = Category(name="Electronics")
        category.save()
        brand = Brand(name="Bata")
        brand.save()
        product.category = category
        product.brand = brand
        product.category = category
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
        product_id = self.kwargs['pk']
        request_for = Product.objects.get(id=product_id)
        responsedata = {
        'id' : request_for.id,
        'name': request_for.name,
        'price': request_for.price,
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
        name = data['name']
        product_id = kwargs['pk']
        category = data['category']
        quantity = data['quantity']
        color = data['color']
        material = data['material']
        brand = data['brand']
        price = data['price']
        description = data['description']
        product = Product.objects.get(id=product_id)
        category = Category(name="Electronics")
        category.save()
        brand = Brand(name="Bata")
        brand.save()
        product.category = category
        product.name = name
        product.quantity = quantity
        product.image = request.FILES['image']
        product.color = color
        product.material = material
        product.brand = brand
        product.price = price
        product.description = description
        product.save()
        return redirect("/product/listproducts/")