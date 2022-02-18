from django.urls import path

from acc.views import ApprovalView, IndexView, ProfileView ,MyUserUpdateView , RejectView
from . import views


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('approval/<int:id>',ApprovalView.as_view(),name='approval'),
    path('profile/<int:pk>', ProfileView.as_view() , name ='profile'),
    path('editdetails/<int:pk>' , MyUserUpdateView.as_view() , name ='update_view'),
    path('reject/<int:pk>', RejectView.as_view(), name = "reject" ),
    #path('approval/' ,ApprovalResultView.as_view(), name="postapproval"),
    
    #path('approval/response/<int:id>',App)
    path('requests' , views.AllReqView.as_view() , name = "getallrequests")

]