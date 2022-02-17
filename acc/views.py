
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,HttpResponseRedirect

from .models import MyUser
from .forms import EditForm, MyLoginForm , AdminAppForm


# Create your views here.
def index(request):
    return render(request, 'blankbody.html')

def approval(request,id = None):
    if request.method == "POST":
        form = AdminAppForm(request.POST)
        ans = form['status'].value()
        if ans == "approve":
            id = request.POST['id']
            MyUser.objects.filter(id = id).update(is_active = True)
        else:
            print("Rejected")
        return HttpResponse("okay")

        
        
    
    else:
        form = AdminAppForm()
        return render(request , 'approval.html' , {'form' : form , 'id' : id})



def profile(request):
    if request.user.is_authenticated:
        current_user = request.user
        context = {'user' : current_user}
        return render(request , 'profile.html')
    else:
        return HttpResponseRedirect('/accounts/login')

def editdetails(request):
    form = EditForm()
    return render(request, 'editprofile.html' , {'form' : form})

def update_view(request):
    current_user = request.user
    id = current_user.id
    
    context ={}
    obj = get_object_or_404(MyUser, id = id)
    form  = MyLoginForm()
    form = EditForm(request.POST or None, instance = obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request , 'profile.html')
   
    return render(request , 'editprofile.html' , {'form' : form })

