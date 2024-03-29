from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm, ValidationError
from .models import *


class DateInput(forms.DateInput):
    input_type = "date"


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ImageReceiptForm(forms.ModelForm):
    class Meta:
        model = Uploaded_Image_Expenses
        fields = "__all__"


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = "__all__"

class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ["expense_name", "total_amount", "date_added", "category"]

        widgets = {"date_added": DateInput()}
