from django.shortcuts import render, redirect

# Create your views here.

def inicio(request):
    return render(request, 'pages/index.html')

def vacantes(request):
    return render(request, 'pages/vacantes.html')