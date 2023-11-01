from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import *
from .models import *

from django.db.models import Q


from django.http import FileResponse
from fpdf import  FPDF

import time

import requests

# AUTH

def Register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account Created For " + user)
                return redirect('login')
            
    context = {"form": form}
    return render(request, "expenses/register.html")

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username or Password is Incorrect")
    return render(request, "expenses/login.html")

def Logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def HomePage(request):
    return render(request, "expenses/homepage.html")

@login_required(login_url='login')
def Upload_Image(request):
    if request.method == 'POST':
        image = request.FILES['image'].read()
        # print(image)
        
        # url = "https://api.mindee.net/v1/products/mindee/expense_receipts/v5/predict"

        # files = {"document": image}
        # print(files)
        # headers = {"Authorization": "Token c2a3493846f7a75257642149578d9d73"}
        # response = requests.post(url, files=files, headers=headers)
        import json
        import requests

        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZmQwNDFlMjctMDc0OS00YjQzLWE1NGQtMDExODg5MjVlMjZlIiwidHlwZSI6ImFwaV90b2tlbiJ9.I5FJVWht-NlNL-CXRzhtMIhbm343lsVO8egGswxEzGY"}

        url="https://api.edenai.run/v2/ocr/data_extraction"
        data={"show_original_response": False,"fallback_providers": "","providers": "base64"}
        files = {'file': image}
        print(files)
        response = requests.post(url, data=data, files=files, headers=headers)

        result = json.loads(response.text)
        print(result)

    return render(request, "expenses/upload_image.html")

@login_required(login_url='login')
def Calculator(request):
    return render(request, "expenses/calculator.html")