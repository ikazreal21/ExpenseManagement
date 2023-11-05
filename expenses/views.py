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
import json


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
    imagereceipt = ImageReceiptForm()
    if request.method == 'POST':
        receiptForm = ImageReceiptForm(request.POST, request.FILES)
        if receiptForm.is_valid():
            image = receiptForm.save()
            # OCR
            url = "https://base64.ai/api/scan"

            payload = json.dumps({
            "url": image.image.url
            })
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'ApiKey jzbsoriano@iskolarngbayan.pup.edu.ph:7871a591-62c6-4817-90e8-f66a061087bd'
            }

            response = requests.request("POST", url, headers=headers, data=payload, timeout=10000)

            result = json.loads(response.text)
            
            keywords = Keywords.objects.all()
            if len(result):
                for i in keywords:
                    if i.keywords.lower() in result[0]['ocr'].lower():
                        print('{0} found'.format(i))
                        if result[0]['fields']['total']:
                            # print("result2", result)
                            print(type(result[0]['fields']['total']['value']))
                            total_amount = result[0]['fields']['total']['value']
                            total_amount = total_amount.replace(',', '')
                            Expenses.objects.create(
                                user=request.user, 
                                expense_name=i.keywords.title(),
                                total_amount=float(total_amount),
                                rndid=image.reference_number,
                                category=i.category
                            )
                            print(result[0]['fields']['total']['value'])
                            return redirect('expenses')
                        else:
                            messages.info(request, "Can't Read Total Amount")
            else:
                Uploaded_Image_Expenses.objects.delete(
                    reference_number=image.reference_number
                )
                messages.info(request, "Receipt Can't Read by the OCR")
    context = {'form': imagereceipt}
    return render(request, "expenses/upload_image.html", context)

@login_required(login_url='login')
def Calculator(request):
    return render(request, "expenses/calculator.html")


@login_required(login_url='login')
def ManageUpload(request):
    expenses = Expenses.objects.filter(user=request.user)
    context = {'expenses': expenses}
    return render(request, "expenses/expenses.html", context)