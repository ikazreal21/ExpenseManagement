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
import datetime

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
            
                system_messages = messages.get_messages(request)
                for message in system_messages:
                    # This iteration is necessary
                    pass


                messages.success(request, "Account Created For " + user)
                return redirect('login')
            else:
                system_messages = messages.get_messages(request)
                for message in system_messages:
                    # This iteration is necessary
                    pass
                messages.info(request, "Make Sure your Credentials is Correct or Valid")
            
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
    today = datetime.datetime.now()
    today2 = datetime.datetime.today()
    days =  datetime.timedelta(days=7)
    print(today2-datetime.timedelta(days=7))

    data_last_seven_days = Expenses.objects.filter(
        date_added__range=(today2-days, today2)
    ).order_by('date_added')
    print("data", data_last_seven_days)

    total_data_last_seven_days = [0] * len(data_last_seven_days)
    uploads = Uploaded_Image_Expenses.objects.filter(user=request.user)
    catergory1 = ExpensesCategory.objects.all()
    expenses = Expenses.objects.filter(user=request.user)
    total_per_month = 0
    total_expenses = 0
    total_expenses_per_month = [0,0,0,0,0,0,0,0,0,0,0,0]
    catergory = []
    catergory_expenses = [0] * len(catergory1)
    print(catergory_expenses)
    counter = 0
    
    for i in catergory1:
        catergory.append(i.category)
        categ_expenses = Expenses.objects.filter(user=request.user, category=i)
        for j in categ_expenses:
            print(counter)
            if j.category == i.category:
                print(categ_expenses)
                catergory_expenses[counter] += j.total_amount
        counter = counter + 1



    for i in expenses:
        print(i.date)
        for j in range(0,13): 
            if j == i.date_added.month:
                total_expenses_per_month[j-1] += i.total_amount

        total_expenses += i.total_amount
        if today.month == i.date_added.month:
            total_per_month += i.total_amount

    initialdate =  data_last_seven_days[0].date_added
    counter = 0
    for i in data_last_seven_days:
        print(initialdate.strftime('%Y-%m-%d'))
        print(i.date_added.strftime('%Y-%m-%d'))

        if initialdate.strftime('%Y-%m-%d') == i.date_added.strftime('%Y-%m-%d'):
            print("date match")
            total_data_last_seven_days[counter] += i.total_amount
        else:
            counter += 1
            initialdate += datetime.timedelta(days=1)
            total_data_last_seven_days[counter] = i.total_amount
    
    print(total_data_last_seven_days)
    
    
    total_amount = float(total_per_month)
    total_per_month = "₱ {:,.2f}".format(total_amount)
    
    total_amount = float(total_expenses)
    total_expenses = "₱ {:,.2f}".format(total_amount)
    
    print(total_per_month)
    print(total_expenses)
    print(catergory)
    print(catergory_expenses)
    context = {'total_per_month': total_per_month,
               'total_expenses': total_expenses,
               'total_expenses_per_month': total_expenses_per_month,
               'uploads': len(uploads),
               'catergory': len(catergory),
               'chart_category': catergory,
               'chart_category_epenses':catergory_expenses,
               'total_data_last_seven_days': total_data_last_seven_days,
               'total_today':total_data_last_seven_days[0] }
            
    return render(request, "expenses/homepage.html", context)

@login_required(login_url='login')
def Upload_Image(request):
    system_messages = messages.get_messages(request)
    for message in system_messages:
        # This iteration is necessary
        pass
    imagereceipt = ImageReceiptForm()
    if request.method == 'POST':
        receiptForm = ImageReceiptForm(request.POST, request.FILES)
        if receiptForm.is_valid():
            receiptForm.save(commit=False).user = request.user
            image = receiptForm.save()
            # # OCR
            url = "https://base64.ai/api/scan"

            payload = json.dumps({
            "url": image.image.url
            })
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'ApiKey joaquinzaki21@gmail.com:c3e7596b-6f0f-456e-b8eb-d96d1dcc553c'
            }

            response = requests.request("POST", url, headers=headers, data=payload, timeout=10000)

            result = json.loads(response.text)
            
            print(result)

            keywords = Keywords.objects.all()
            if len(result):
                for i in keywords:
                    if i.keywords.lower() in result[0]['ocr'].lower():
                        print('{0} found'.format(i))
                        if 'total' in result[0]['fields']:
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
                                return redirect('upload_confirmation', pk=image.reference_number)
                        elif 'heightImperial' in result[0]['fields']:
                            print(type(result[0]['fields']['heightImperial']['value']))
                            total_amount = result[0]['fields']['heightImperial']['value']
                            total_amount = total_amount.replace(',', '')
                            if total_amount == '':
                                total_amount = 0
                            Expenses.objects.create(
                                user=request.user, 
                                expense_name=i.keywords.title(),
                                total_amount=float(total_amount),
                                rndid=image.reference_number,
                                category=i.category
                            )
                            return redirect('upload_confirmation', pk=image.reference_number)
                        else:
                            Expenses.objects.create(
                                user=request.user, 
                                expense_name=i.keywords.title(),
                                total_amount=float(0),
                                rndid=image.reference_number,
                                category=i.category
                            )
                            return redirect('upload_confirmation', pk=image.reference_number)
                messages.info(request, "Receipt Can\'t Read by the OCR")
                return redirect('upload_confirmation', pk=image.reference_number)
            else:
                # Uploaded_Image_Expenses.objects.get(
                #     reference_number=image.reference_number
                # ).delete()
                system_messages = messages.get_messages(request)
                for message in system_messages:
                    # This iteration is necessary
                    pass
                messages.info(request, "Receipt Can\'t Read by the OCR")
                return redirect('upload_confirmation', pk=image.reference_number)
    context = {'form': imagereceipt}
    return render(request, "expenses/upload_image.html", context)

@login_required(login_url='login')
def Calculator(request):
    return render(request, "expenses/calculator.html")

@login_required(login_url='login')
def Upload_Image_Confirmation(request, pk):
    catergory = ExpensesCategory.objects.all()
    expenses = Expenses.objects.get(rndid=pk)
    receipt = Uploaded_Image_Expenses.objects.get(
            reference_number=pk
        )
    stockform = ExpenseForm(instance=expenses)
    print(stockform)
    if request.method == 'POST':
        stockform = ExpenseForm(request.POST, request.FILES, instance=expenses)
        if stockform.is_valid():
            print(stockform)
            stockform.save(commit=False).user = request.user
            stockform.save()
            return redirect('expenses')
    context = {"expense": expenses, "image": receipt, "category": catergory}
    return render(request, "expenses/view_upload_confirmation.html", context)

@login_required(login_url='login')
def Cancel(request, pk):
    upload = Uploaded_Image_Expenses.objects.get(
        reference_number=pk
    )
    expenses = Expenses.objects.get(
        rndid=pk
    )
    upload.delete()
    expenses.delete()
    return redirect('upload_reciept')

@login_required(login_url='login')
def Delete(request, pk):
    upload = Uploaded_Image_Expenses.objects.get(
        reference_number=pk
    )
    expenses = Expenses.objects.get(
        rndid=pk
    )
    upload.delete()
    expenses.delete()
    return redirect('expenses')

@login_required(login_url='login')
def Update(request, pk):
    catergory = ExpensesCategory.objects.all()
    expenses = Expenses.objects.get(rndid=pk)
    receipt = Uploaded_Image_Expenses.objects.get(
            reference_number=pk
        )
    stockform = ExpenseForm(instance=expenses)
    print(stockform)
    if request.method == 'POST':
        stockform = ExpenseForm(request.POST, request.FILES, instance=expenses)
        print(stockform)
        if stockform.is_valid():
            stockform.save(commit=False).user = request.user
            stockform.save()
            return redirect('expenses')
    context = {"expense": expenses, "image": receipt, "category": catergory}
    return render(request, "expenses/update_upload.html", context)

@login_required(login_url='login')
def View(request, pk):
    catergory = ExpensesCategory.objects.all()
    expenses = Expenses.objects.get(rndid=pk)
    receipt = Uploaded_Image_Expenses.objects.get(
            reference_number=pk
        )
    context = {"expense": expenses, "image": receipt, "category": catergory}
    return render(request, "expenses/view_upload.html", context)

@login_required(login_url='login')
def ManageUpload(request):
    expenses = Expenses.objects.filter(user=request.user)
    category = ExpensesCategory.objects.all()

    if request.method == 'POST':
        category1 = request.POST.get('category')
        if category1 != "":
            expenses = Expenses.objects.filter(user=request.user, category=category1)
            context = {'expenses': expenses, "category": category}


    context = {'expenses': expenses, "category": category}
    return render(request, "expenses/expenses.html", context)