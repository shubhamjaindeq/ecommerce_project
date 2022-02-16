from audioop import reverse
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from .forms import EditForm, MyLoginForm
from .models import MyUser

# Create your views here.
def index(request):
    return render(request, 'blankbody.html')

def profile(request):
    if request.user.is_authenticated:
        current_user = request.user
        print(current_user.full_name)
        context = {'user' : current_user}
        return render(request , 'profile.html')
    else:
        return HttpResponseRedirect('/accounts/login')

def editdetails(request):
    form = EditForm()
    return render(request, 'editprofile.html' , {'form' : form})

def update_view(request):
    current_user = request.user
    print("front")
    id = current_user.id
    print(id)
    context ={}
    obj = get_object_or_404(MyUser, id = id)
    form  = MyLoginForm()
    form = EditForm(request.POST or None, instance = obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(request , 'profile.html')
   
    return render(request , 'editprofile.html' , {'form' : form })

