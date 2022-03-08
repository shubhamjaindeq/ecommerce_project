"""urls mapping for acc app file"""
from django.urls import path

from order.views import AddToCartView, CartView, DeleteFromCartView, CheckoutView, MyOrdersView, CancelOrderView, OrderDetailView, RemoveItemView, BuyNowView, ShopOrderView, ItemStatusUpdateView


urlpatterns = [

    path('addtocart/<int:pk>', AddToCartView.as_view(), name = "addtocart"),
    path('mycart/<int:pk>', CartView.as_view(), name = "mycart"),
    path('deletefromcart/', DeleteFromCartView.as_view(), name="deletefromcart"),
    path('checkout/', CheckoutView.as_view(), name = "checkout"),
    path('myorders/', MyOrdersView.as_view(), name = "myorders"),
    path('cancelorder/<int:pk>', CancelOrderView.as_view(), name = "cancelorder"),
    path('orderdetail/<int:pk>', OrderDetailView.as_view(), name = "orderdetail"),
    path('removeitem/<int:pk>', RemoveItemView.as_view(), name = "removeitem"),
    path("buynow/<int:pk>", BuyNowView.as_view(), name = "buynow"),
    path('shoporder/', ShopOrderView.as_view(), name = "shoporder"),
    path('itemstatusupdate/<int:pk>', ItemStatusUpdateView.as_view(), name = "itemstatusupdate"),
]
