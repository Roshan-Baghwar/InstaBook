from django.shortcuts import render
import UserService

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    return UserService.signup(request)