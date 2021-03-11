from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import *


# for staff

# views/category
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

# views/new_product
class ProductForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['price'] = forms.DecimalField(min_value=0, decimal_places=2, max_digits=10, label="Price")
    
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['date_created']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 8}),
        }


# for all staff and customers

# views/checkout
class OrderForm(forms.Form):

    STORE = [
        ('', ''),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]
	
    STAY = [
        ('Stay', 'Stay'),
        ('Takeaway', 'Takeaway'),
    ]

    store = forms.ChoiceField(label='Store:', widget=forms.Select, choices=STORE, required=True)
    stay = forms.ChoiceField(label='Stay or Take away?', widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}), choices=STAY, required=True) # stay in or takeaway
    name = forms.CharField(label='Your name', required=False)
    phone = forms.CharField(label='Phone', max_length=8, min_length=8, widget=forms.TextInput(attrs={'placeholder': '+852'}), required=True) # using Hong Kong phone num
    email = forms.EmailField(label='Email', required=True)

class StaffOrderForm(forms.Form):
    STORE = [
        ('', ''),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]
	
    STAY = [
        ('Stay', 'Stay'),
        ('Takeaway', 'Takeaway'),
    ]

    store = forms.ChoiceField(label='Store:', widget=forms.Select, choices=STORE, required=True)
    stay = forms.ChoiceField(label='Stay or Take away?', widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}), choices=STAY, required=True) # stay in or takeaway
