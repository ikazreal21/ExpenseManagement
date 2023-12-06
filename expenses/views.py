from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from django.core.files import File
from django.db.models import Sum

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

from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

def generate_invoice_pdf(invoice_data, username, output_filename='invoice.pdf'):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    title_style = getSampleStyleSheet()['Title']
    elements.append(Paragraph("Report Generated", title_style))

    invoice_style = ParagraphStyle('InvoiceStyle', parent=getSampleStyleSheet()['BodyText'], spaceAfter=15)
    elements.append(Paragraph("Report Details:", invoice_style))

    table_data = [['Expenses Name', 'Category', 'Date', 'Total']]
    for item in invoice_data:
        total_amount = float(item.total_amount)
        total_amountstr = "{:,.2f}".format(total_amount)
        table_data.append([item.expense_name, item.category, item.date(), total_amountstr])

    

    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table = Table(table_data, style=table_style)
    elements.append(table)

    total = sum(item.total_amount for item in invoice_data)
    total_amount = float(total)
    total_amountstr = "\u20B1 {:,.2f}".format(total_amount)
    elements.append(Paragraph(f"Total: {total_amountstr}", invoice_style))

    doc.title = f"{username} generated report"

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    return pdf

def create_rand_id():
        from django.utils.crypto import get_random_string
        return get_random_string(length=13, 
            allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')


from roboflow import Roboflow
rf = Roboflow(api_key="He28uTlpoqBXsFA1hHxS")
project = rf.workspace().project("receipt-logo-detection")
model = project.version(3).model

# infer on a local image 
# print(model.predict("your_image.jpg", confidence=40, overlap=30).json())

# visualize your prediction
# model.predict("your_image.jpg", confidence=40, overlap=30).save("prediction.jpg")

# infer on an image hosted elsewhere
# print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())

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
    day = today2.day
    month = today2.month
    year = today2.year

    total_per_month = 0
    total_expenses = 0
    total_expenses_per_month = [0,0,0,0,0,0,0,0,0,0,0,0]
    catergory = []    
    total_data_last_seven_days = []
    date_last_seven_days = []

    uploads = Expenses.objects.filter(user=request.user)
    total_today = Expenses.objects.filter(user=request.user, date_added__year=year, date_added__month=month, date_added__day=day)

    expenses = Expenses.objects.filter(user=request.user, date_added__year=year)

    # Category
    catergory1 = ExpensesCategory.objects.all()
    catergory_expenses = [0] * len(catergory1)
    
    counter = 0
    for i in catergory1:
        catergory.append(i.category)
        categ_expenses = Expenses.objects.filter(user=request.user, category=i)
        for j in categ_expenses:
            if j.category == i.category:
                catergory_expenses[counter] += j.total_amount
        counter = counter + 1



    for i in expenses:
        for j in range(0,13): 
            if j == i.date_added.month:
                total_expenses_per_month[j-1] += i.total_amount

        total_expenses += i.total_amount
        if today.month == i.date_added.month:
            total_per_month += i.total_amount

    last_7_days = today2-datetime.timedelta(days=7)

    last_seven_days = Expenses.objects.filter(user=request.user, date_added__gte=last_7_days).\
    extra({'day':"date_added"}).\
    values('day').annotate(count=Sum('total_amount'))

    for i in last_seven_days:
        date = datetime.datetime.fromisoformat(str(i["day"])[:-6])
        formatted_date = date.strftime("%B %d, %Y")
        total_data_last_seven_days.append(i["count"])
        date_last_seven_days.append(formatted_date)
    
    print(date_last_seven_days)

    tolal_today_amount = 0

    for amount in total_today:
        tolal_today_amount += amount.total_amount

    
    
    total_amount = float(total_per_month)
    total_per_month = "₱ {:,.2f}".format(total_amount)
    
    total_amount = float(total_expenses)
    total_expenses = "₱ {:,.2f}".format(total_amount)
    
    total_today = float(tolal_today_amount)
    total_today = "₱ {:,.2f}".format(total_today)

    context = {'total_per_month': total_per_month,
               'total_expenses': total_expenses,
               'total_expenses_per_month': total_expenses_per_month,
               'uploads': len(uploads),
               'catergory': len(catergory),
               'chart_category': catergory,
               'chart_category_epenses':catergory_expenses,
               'total_data_last_seven_days': total_data_last_seven_days,
               'date_last_seven_days': date_last_seven_days,
               'total_today': total_today }
            
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
        # print(timezone.now)
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
            'Authorization': 'ApiKey soriano.zaki.1@gmail.com:26923409-5d6f-4687-8341-97a60dc223e1'
            }

            response = requests.request("POST", url, headers=headers, data=payload, timeout=10000)

            result = json.loads(response.text)

            model.predict(image.image.url, hosted=True, confidence=40, overlap=30).save("expenses\prediction\prediction.jpg")
            prediction_result = model.predict(image.image.url, hosted=True, confidence=40, overlap=30).json()

            if prediction_result:
                image.image.save('prediction.jpg', File(open('expenses\prediction\prediction.jpg', 'rb')))

            print(result)
            print(prediction_result)
            prediction = ''
            if 'class' in prediction_result:
                prediction= prediction_result["predictions"][0]["class"]
            keywords = Keywords.objects.all()
            if len(result):
                for i in keywords:
                    if i.keywords.lower() in prediction.lower() or \
                        i.keywords.lower() in result[0]['ocr'].lower():
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
                messages.info(request, "Invalid Reciept")
                return redirect('upload_reciept')
            else:
                # Uploaded_Image_Expenses.objects.get(
                #     reference_number=image.reference_number
                # ).delete()
                system_messages = messages.get_messages(request)
                for message in system_messages:
                    # This iteration is necessary
                    pass
                messages.info(request, "Invalid Reciept")
                return redirect('upload_reciept')
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
        print(stockform)
        if stockform.is_valid():
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
    upload = Uploaded_Image_Expenses.objects.filter(
        reference_number=pk
    )
    expenses = Expenses.objects.get(
        rndid=pk
    )
    if upload:
        upload.delete()
    expenses.delete()
    return redirect('expenses')

@login_required(login_url='login')
def Update(request, pk):
    catergory = ExpensesCategory.objects.all()
    expenses = Expenses.objects.get(rndid=pk)
    receipt = Uploaded_Image_Expenses.objects.filter(
            reference_number=pk
        )
    stockform = ExpenseForm(instance=expenses)
    print(stockform)
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            receiptForm = ImageReceiptForm(request.POST, request.FILES)
            print(receiptForm)
            if receiptForm.is_valid():
                receiptForm.save(commit=False).user = request.user
                receiptForm.save(commit=False).reference_number = pk
                image = receiptForm.save()
                return redirect('expenses')
        stockform = ExpenseForm(request.POST, request.FILES, instance=expenses)
        print(stockform)
        if stockform.is_valid():
            stockform.save(commit=False).user = request.user
            stockform.save()
            return redirect('expenses')
    if receipt:
        context = {"expense": expenses, "image": receipt[0], "category": catergory}
    else:
        context = {"expense": expenses, "category": catergory}
    return render(request, "expenses/update_upload.html", context)

@login_required(login_url='login')
def View(request, pk):
    catergory = ExpensesCategory.objects.all()
    expenses = Expenses.objects.get(rndid=pk)
    receipt = Uploaded_Image_Expenses.objects.filter(
            reference_number=pk
        )
    if receipt:
        context = {"expense": expenses, "image": receipt[0], "category": catergory}
    else:
        context = {"expense": expenses, "category": catergory}
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

@login_required(login_url='login')
def AddExpenses(request):
    catergory = ExpensesCategory.objects.all()
    print(create_rand_id())
    if request.method == 'POST':
        image = request.FILES.get('image')
        print(image)
        expense_name = request.POST.get('expense_name')
        category = request.POST.get('category')
        date_added = request.POST.get('date_added')
        total_amount = request.POST.get('total_amount')
        if image:
            receiptForm = ImageReceiptForm(request.POST, request.FILES)
            print(receiptForm)
            if receiptForm.is_valid():
                receiptForm.save(commit=False).user = request.user
                image = receiptForm.save()
                Expenses.objects.create(
                    user=request.user, 
                    expense_name=expense_name,
                    total_amount=float(total_amount),
                    rndid=image.reference_number,
                    category=category,
                    date_added=date_added
                )
                return redirect('expenses')
        else:
            stockform = AddExpenseForm(request.POST)
            print(stockform)
            if stockform.is_valid():
                print(stockform)
                stockform.save(commit=False).user = request.user
                rand_id = create_rand_id()
                if image:
                    print("image")
                    stockform.save(commit=False).rndid = image.reference_number
                else: 
                    stockform.save(commit=False).rndid = str(rand_id)
                stockform.save()
                return redirect('expenses')
    context = {"category": catergory}
    return render(request, "expenses/manual_add.html", context)

@login_required(login_url='login')
def Report(request):
    if request.method == 'POST':
        report_name = request.POST.get("expense_name")
        filter_date = request.POST.get("filter")
        date_added = request.POST.get("date_added")
        dateobject = datetime.datetime.strptime(date_added, '%Y-%m-%d').date().day
        print(dateobject)
        print(filter_date)
        print(report_name)

        if filter_date == "Year":
            year = datetime.datetime.strptime(date_added, '%Y-%m-%d').date().year

            uploads = Expenses.objects.filter(user=request.user, date_added__year=year)
        elif filter_date == "Month":
            year = datetime.datetime.strptime(date_added, '%Y-%m-%d').date().year
            month = datetime.datetime.strptime(date_added, '%Y-%m-%d').date().month

            uploads = Expenses.objects.filter(user=request.user, date_added__year=year, date_added__month=month)
        
        else:
            year = datetime.datetime.strptime(date_added, '%Y-%m-%d').date().year
            month = datetime.datetime.strptime(date_added, '%Y-%m-%d').date().month
            day = datetime.datetime.strptime(date_added, '%Y-%m-%d').date().day

            uploads = Expenses.objects.filter(user=request.user, date_added__year=year, date_added__month=month, date_added__day=day)

        pdf = generate_invoice_pdf(uploads, request.user)

        # Create HTTP response with PDF content
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(report_name)
        # Render a template with JavaScript for redirection
        template = get_template('expenses/redirect_template.html')
        context = {'redirect_url': reverse('expenses')}
        response.write(template.render(context, request))

        return response
    
    context = {}
    return render(request, "expenses/generate_report.html", context)


