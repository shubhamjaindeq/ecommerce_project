from django.shortcuts import render
"""program logic for the acc app"""
import json
import datetime

from django.views import View
from django.db.models import F
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from dashboard.filters import ProductFilter, SalesFilter
from acc.models import User
from product.models import Product
#, Wishlist, Cart, CartItems, Order, OrderItems , Brand, Category


# Create your views here.
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
                {'productlist': page_obj, 'productFilter' : productfilter, 'products': productlist }
            )

        elif request.user.role == "shopowner":
            #return redirect('/listproducts')
            return render(request,'shop/shopindex.html' )
        else:
            return render(request,'adminindex.html' )
