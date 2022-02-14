from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # path('registration/',include('registration.backends.admin_approval.urls')),
    path('acc/',include('acc.urls')),

]
