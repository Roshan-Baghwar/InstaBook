from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import UserService

# Create your views here.

@login_required(login_url='signin')
def index(request):
    return UserService.index(request)

def signup(request):
    return UserService.signup(request)

def signin(request):
    return UserService.signin(request)

@login_required(login_url='signin')
def post(request):
    return UserService.post(request)

@login_required(login_url='signin')
def likepost(request):
    return UserService.likepost(request)

@login_required(login_url='signin')
def logout(request):
    return UserService.logout(request)