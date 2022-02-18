
from pipes import Template
from re import template
from urllib import request
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.shortcuts import render,get_object_or_404,HttpResponseRedirect

from .models import MyUser
from .forms import EditForm, MyLoginForm , AdminAppForm


# Create your views here.
class IndexView(TemplateView):

    template_name = "blankbody.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ApprovalView(TemplateView):

    template_name = 'approval.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']

        user = MyUser.objects.get(id=id)
        context['user'] = user
        form = AdminAppForm()
        context['form'] = form
        return context
    





class RejectView(DeleteView):
    model = MyUser
    success_url = '/acc'
    template_name = 'comfirmdelete.html'
    form_class = AdminAppForm
    def form_valid(self, form):
        print(form['response'].value(), "is response")
        
        success_url = self.get_success_url()
        if form['response'].value() == "reject":
            self.object.delete()
            return HttpResponse(success_url)
        else:
            intended_user = MyUser.objects.get(id = self.kwargs['pk'])
            intended_user.is_active = True
            intended_user.save()
            print(self.kwargs)
            return HttpResponseRedirect(success_url)


class ProfileView(DetailView):
    model = MyUser
    template_name = 'profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user)
        context['user'] = self.request.user
        print(context)
        return context

class AllReqView(ListView):
    model = MyUser
    template_name = "myuser_list.html"
    def get_queryset(self):
        return MyUser.objects.filter(is_active = False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lst'] = MyUser.objects.filter(is_active = False)
        return context
            
class MyUserUpdateView(UpdateView):
    model = MyUser
    template_name = 'editprofile.html'
    fields = [
        "full_name",
        "address",
        "date_of_birth",
        "email",
    ]
  
    
    success_url ="/acc"

