from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from .forms import EditForm, MyLoginForm
from .models import MyUser

# Create your views here.
def index(request):
    return render(request, 'blankbody.html')

def profile(request):

    return render(request , 'profile.html')

def editdetails(request):
    form = EditForm()
    return render(request, 'editprofile.html' , {'form' : form})

def update_view(request):
    current_user = request.user
    print("front")
    id = current_user.id
    print(id)
    print("break")
    context ={}
    obj = get_object_or_404(MyUser, id = id)
 
    print(obj)
    form  = MyLoginForm()
    print(form)
    form = EditForm(request.POST or None, instance = obj)
    print(form)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("running")
    print(form)
    return render(request , 'editprofile.html' , {'form' : form })