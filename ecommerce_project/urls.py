from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    #path('accounts/signupshop', views.signupasshop , ),
    path('acc/',include('acc.urls')),

]
