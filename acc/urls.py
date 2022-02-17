from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile , name ='profile'),
    path('editdetails/' , views.update_view , name ='update_view'),
    path('approval' , views.approval, name="postapproval"),
    path('approval/<int:id>',views.approval,name='approval'),

]