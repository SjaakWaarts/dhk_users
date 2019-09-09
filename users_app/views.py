import re
from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.models import User
import django.contrib.auth as auth

from users_app.forms import LogMessageForm
from users_app.forms import RegisterForm
from users_app.models import LogMessage

# Create your views here.

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "users_app/log_message.html", {"form": form})

def about(request):
    return render(request, "users_app/about.html")

def contact(request):
    return render(request, "users_app/contact.html")

def user_register(request):
    # if this is a POST request we need to process the form data
    template = 'registration/register.html'
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form, 
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form, 
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form, 
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user: 
                user = User.objects.create_user(
                    form.cleaned_data['username'], 
                    form.cleaned_data['email'], 
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.save()
                
                # Login the user
                auth.login(request, user)
                
                # redirect to accounts page:
                return HttpResponseRedirect(reverse('home'))

   # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})     
