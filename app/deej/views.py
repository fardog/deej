from django.template import Context, loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import login as auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms


class DeejAuthForm(AuthenticationForm):
        username = forms.CharField(max_length=64, widget=forms.HiddenInput)
        password = forms.CharField(widget=forms.PasswordInput)


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/recording/')
    else:
        return HttpResponseRedirect('/login/')


def login(request):
    view_data = {}
    view_data['users'] = User.objects.order_by('-last_login')

    login_form = DeejAuthForm(data=(request.POST or None))
    if request.method == "POST" and login_form.is_valid():
        auth(request, login_form.get_user())
        return HttpResponseRedirect('/')

    return render(request, 'deej.login.html', {'login_form': login_form, 'view_data': view_data, })


def register(request):
    view_data = {}

    register_form = UserCreationForm(request.POST or None)
    if request.method == "POST" and register_form.is_valid():
        register_form.save()
        return HttpResponseRedirect('/')

    return render(request, 'deej.register.html', {'register_form': register_form, 'view_data': view_data, })
