"""urls mapping for acc app file"""
from django.urls import path

from product.views import ProductDetailView, AddToWishlistView , WishListView, \
     DeleteFromWishListView, AddProductFormView, ProductListView, ProductUpdateView, ProductDeleteView


urlpatterns = [
   
    path('deleteproduct/', ProductDeleteView.as_view(), name = "deleteproduct"),
    path('productdetail/<int:pk>', ProductDetailView.as_view(), name='profile'),
    path('addtowishlist/<int:pk>', AddToWishlistView.as_view(), name = 'addtowishlist'),
    path('mywishlist/<int:pk>', WishListView.as_view(), name="mywishlist"),
    path('deletefromwishlist/', DeleteFromWishListView.as_view(), name="deletefromwishlist"),
     path('addproduct/', AddProductFormView.as_view(), name = 'addproduct'),
    path('listproducts/', ProductListView.as_view(), name = "productlist" ),
    path('productupdate/<int:pk>', ProductUpdateView.as_view(), name = "productupdate"),
    

]
