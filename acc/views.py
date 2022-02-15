from django.http import HttpResponse
from django.shortcuts import render
from .forms import EditForm

# Create your views here.
def index(request):
    return render(request, 'blankbody.html')

def profile(request):

    return render(request , 'profile.html')

def editdetails(request):
    form = EditForm()
    return render(request, 'editprofile.html' , {'form' : form})