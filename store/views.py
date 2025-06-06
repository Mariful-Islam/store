
from django.shortcuts import redirect, render


def home(request):
    return redirect('swagger-schema')


def index(request):

    return render(request, 'index.html')