"""program logic for the acc app"""
import json
from django.core.paginator import Paginator
from django.views import View
from django.db.models import Q
from django.http import JsonResponse 
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .filters import ProductFilter
from .models import User , Product , Wishlist , Cart , CartItems
from .forms import RequestResponseForm, ShopSignupForm , AddUserForm , AdminUserUpdateForm , AddShop


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
                print("lgkj")
                keyword = request.GET.get('search')
                print(keyword)
                productlist = productlist.filter(Q(name__icontains=keyword) | Q(description__icontains = keyword ))
                print(productlist)
            if request.GET.get('sortby') == "plth":
                print("plth")
                productlist = productlist.order_by('price')
            elif request.GET.get('sortby') == "phtl":
                productlist = productlist.order_by('-price')
            elif request.GET.get('sortby') == "rlth":
                productlist = productlist.order_by('rating')
            else:
                productlist = productlist.order_by('-rating')
            
            productFilter = ProductFilter(request.GET, queryset=productlist)
            
            productlist = productFilter.qs
            
            paginator = Paginator(productlist, 1)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            return render(request,self.template_name , {'productlist': page_obj , 'productFilter' : productFilter } )
        
        elif request.user.role == "shopowner":
            return render(request,'shop/shopindex.html' )

        else:
            return render(request,'adminindex.html' )

        


        



class CustomerLandingView(ListView):

    model = Product
    template_name = "customerindex.html"

class ShopLanding(ListView):

    model = Product
    template_name = "shopindex.html"


class ApprovalView(View):
    """handles rendering and fetching of form for admin to accept and reject
    requests"""
    form_class = RequestResponseForm
    template_name = 'requestresponse.html'

    def get(self, request , *args , **kwargs):
        """gets called if the request methods is get"""
        user_id = self.kwargs['id']
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
                print("reject called")
                request_by.delete()

            return redirect('/requests')

class UserListView(ListView):
    """admin gets a list of user"""
    template_name = 'userlist.html'
    model = User

class ProductListView(ListView):
    """admin gets a list of user"""
    template_name = 'shop/productlist.html'
    model = Product

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        products = Product.objects.filter(provider=self.request.user)
        print(products)
        #breakpoint()
        return products 
        

class UserProfileView(DetailView):
    """Handles My profile view for customer"""
    model = User
    template_name = 'customer/profile.html'

class ShopProfileView(DetailView):
    """Handles My profile view for customer"""
    model = User
    template_name = 'shop/profile.html'

class RequestsView(ListView):
    """collect all pending requests and show it to amdin"""
    model = User
    template_name = "requestlist.html"
    context_object_name = 'lst'

    def get_queryset(self):
        """only show those users who have is_active = False"""
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
    """Renders and handles form for registration of shop"""
    form_class = AddUserForm
    template_name = "adduser.html"
    success_url ="/"

    def form_valid(self, form):
        """verify if the form data is valid and fetch attributes"""
        print(form.cleaned_data)
        user = User()
        user.email = form.cleaned_data['email'] 
        user.password = form.cleaned_data['password2']
        user.set_password(user.password)
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

    def get(self, request , *args , **kwargs):
        user_id = self.kwargs['pk']
        request_by = User.objects.get(id=user_id)
        responseData = {
        'id': request_by.id,
        'full_name': request_by.full_name,
        'email': request_by.email,
        'role' : request_by.role,
        'address' : request_by.address,
    }
        
        return JsonResponse(responseData)

    def post(self , request , *args , **kwargs):
        data = json.loads(request.POST.get('data', ''))
        obj = data['obj']
        id = obj['id']
        address = obj['address']
        full_name = obj['full_name']
        role = obj['role']
        email = obj['email']
        request_by = User.objects.get(id=id)
        request_by.address = address
        request_by.full_name = full_name
        request_by.role = role
        request_by.email = email
        request_by.save()
        return HttpResponse("okay")

class UserDeleteByAdmin(View):
    """view for admin to delete users"""

    def post(self , request):
        """recieved post data from ajax"""
        data = json.loads(request.POST.get('data', ''))
        id = data['obj']['id']
        print(id)
        request_by = User.objects.get(id=id)
        request_by.delete()
        
        



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

class AddShopFormView(FormView):
    template_name = 'shop/addshop.html'
    form_class = AddShop
    success_url = '/thanks/'

    def form_valid(self, form):
        id = self.request.user.id
        user = User.objects.get(id=id)
        product = Product()
        product.name = form.cleaned_data['name']
        product.price = form.cleaned_data['price']
        product.description = form.cleaned_data['description']
        product.image = form.cleaned_data['image']
        product.brand = form.cleaned_data['brand']
        product.category = form.cleaned_data['category']
        product.provider = user
        product.quantity = form.cleaned_data['quantity']
        
        product.save()
        print("saved")
        return redirect('/')
        
class ProductUpdateView(View):

    model = Product
    

    def get(self, request , *args , **kwargs):
        print("product update  clalled")
        user_id = self.kwargs['pk']
        request_for = Product.objects.get(id=user_id)
        responseData = {
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
        
        return JsonResponse(responseData)

    def post(self , request , *args , **kwargs):
        data = request.POST
        print(request.FILES['image'])
        #breakpoint()
        #print("breakpoint")
        #print(data['image'])
        
        name = data['name']
        id = data['id']
        category = data['category']
        quantity = data['quantity']
        color = data['color']
        material = data['material']
        brand = data['brand']
        description = data['description']
        product = Product.objects.get(id=id)
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

    def post(self , request):
        """recieved post data from ajax"""
        data = json.loads(request.POST.get('data', ''))
        id = data['obj']['id']
        print(id)
        request_by = Product.objects.get(id=id)
        request_by.delete()

class ProductDetailView(DetailView):
    """Handles My profile view for customer"""
    model = Product
    template_name = 'customer/productdetail.html'

class BuyProductView(View):
    def get(self , request, **kwargs):

        print(self.kwargs)
        return HttpResponse("bought")

class AddToWishlistView(View):
    def get(self, request, **kwrags):

        product_id = self.kwargs['pk']
        id = request.user.id
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=id)
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

    def get(self,request, **kwrags):
        user_id = request.user.id
        user = User.objects.get(id = user_id)
        wishl = user.wishlist
        object_list = wishl.items.all()
        print(user)
        return render(request, 'customer/mywishlist.html' , { 'object_list' : object_list })

class DeleteFromWishListView(View):

    def post(self,request,**kwargs):
        data = json.loads(request.POST.get('data', ''))
        product_id = data['obj']['id']
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=request.user.id)
        wishl = user.wishlist
        wishl.items.remove(product)
        return redirect('/mywishlist/' + str(request.user.id) )

class AddToCartView(View):

    def get(self, request, **kwargs):
        print("addtocart called" , kwargs)
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
            cartitems =  CartItems(product , 1 , cart)
            cartitems.save()



        return redirect('/mycart/' + str(user.id))


class CartView(ListView):
    template_name = "customer/mycart.html"
    def get_queryset(self):
        print(self.request.user)
        user = self.request.user
        object_list = user.cart.cartitems_set.all()
        return object_list

class DeleteFromCartView(View):

    def post(self,request):
        data = json.loads(request.POST.get('data', ''))
        entry_id = data['obj']['id']
        entry = CartItems.objects.get(id=entry_id)
        entry.delete()
        return redirect('/mycart/' + str(request.user.id) )