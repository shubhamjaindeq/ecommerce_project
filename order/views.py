import datetime
import json
from django.http import JsonResponse

from django.shortcuts import render
from product.models import Product, Wishlist
from order.models import Cart , CartItems, Order, OrderItems
from acc.models import User

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from django.shortcuts import redirect, render
# Create your views here.
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
            cartitems = CartItems(quantity = 1)
            cartitems.product = product
            cartitems.cart = cart
            cartitems.save()
        return redirect('/order/mycart/' + str(user.id))


class CartView(ListView):
    """view for all items in cart"""

    template_name = "customer/mycart.html"

    def get_queryset(self):
        """prepares list view for cart items"""

        if self.request.user.role != "customer":
            return redirect("/accounts/logout")
        user = self.request.user
        if not hasattr(user, 'cart'):
            return redirect("/dashboard")
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
        return redirect('/order/mycart/' + str(request.user.id) )

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
        orderitem.provider = Product.objects.get(id=kwargs['pk']).provider
        orderitem.total = Product.objects.get(id=kwargs['pk']).price
        orderitem.save()
        order.total = orderitem.total
        order.status = "paid"
        order.save()
        return redirect("/order/myorders")

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
            orderitem = OrderItems(
                order=order, item = product, quantity=quantity, total=total,
            )
            orderitem.save()
            product.save()

        order.total = total_price
        order.status = "paid"
        order.save()
        for items in all_items:
            items.delete()
        return redirect("/dashboard")

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
        return redirect("/order/myorders/")

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
        orderitem.delete()
        return redirect("/order/orderdetail/"+order_id)

class ShopOrderView(ListView):
    """fetch orders for a particular shop"""

    template_name = "shop/myorders.html"
    model = OrderItems

    def get_queryset(self):
        """fetch and prepare data for the view"""
        user = User.objects.get(id=self.request.user.id)
        items_list = OrderItems.objects.filter(item__provider = user)
        return items_list

class ItemStatusUpdateView(View):
    """Update item status by shop"""

    model = OrderItems

    def get(self, request, **kwargs):
        """gets called if the request method is get
        and prefills data"""

        if request.user.role != "shopowner":
            return redirect("/accounts/logout")
        order_item = OrderItems.objects.get(id=self.kwargs['pk'])
        responsedata = {
        'id' : order_item.id,
        'status' : order_item.status,
        }
        return JsonResponse(responsedata)

    def post(self, request , **kwargs):
        """gets called if the request method is post and data is updated"""

        if request.user.role != "shopowner":
            return redirect("/accounts/logout")
        data = request.POST
        order_item_id = kwargs['pk']
        new_status = data['status']
        order_item = OrderItems.objects.get(id=order_item_id)
        order_item.status = new_status
        order_item.save()
        return redirect("/product/listproducts/")