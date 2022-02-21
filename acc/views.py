"""program logic for the acc app"""
from re import template
from django.views import View
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import User
from .forms import RequestResponseForm, ShopSignupForm , AddUserForm , AdminUserUpdateForm


class IndexView(TemplateView):
    """Landing page"""
    template_name = 'customer/customerindex.html'
    
    @method_decorator(login_required)
    def get(self, request):
        """gets called if the request methods is get"""
        
        if request.user.role == "shopowner":
                self.template_name = "shop/shopindex.html"
        if request.user.role == "admin":
                self.template_name = "adminindex.html"
        return render(request, self.template_name )

        
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
       return super(self.__class__, self).dispatch(request, *args, **kwargs)

        

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

    template_name = 'userlist.html'
    model = User

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

class UserUpdateByAdminView(UpdateView):

    form_class = AdminUserUpdateForm

    def get(self, request , *args , **kwargs):
        print("user update by admin clalled")
        breakpoint()
        """gets called if the request methods is get"""
        user_id = self.kwargs['id']
        request_by = User.objects.get(id=user_id)
        form = self.form_class()
        return render(request , self.template_name , {'form' : form  , 'request_by' : request_by })



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
