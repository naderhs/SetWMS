from django import forms
from django.contrib.auth.models import User
from set_app import models


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta():
		model = User
		fields = '__all__'


class UserProfileInfoForm(forms.ModelForm):
	class Meta():
		model = models.UserProfileInfo
		fields = '__all__'


class WarehouseForm(forms.Form):
	name = forms.CharField(max_length=30)
	postcode = forms.CharField(max_length=11)


class CustomerForm(forms.Form):
	last_name = forms.CharField(max_length=30)
	company_name = forms.CharField(max_length=30)

class OrderForm(forms.ModelForm):
	class Meta():
		model = models.Order
		fields = ['order_type', 'warehouse', 'customer','permit_type','permit_number','notes']

class OrderInForm(forms.ModelForm):
	class Meta():
		model = models.Order
		fields = ['order_type', 'warehouse', 'customer','permit_type','permit_number','notes']

class ProductForm(forms.ModelForm):
	class Meta():
		model = models.Product
		fields = '__all__'

class TransactionForm(forms.ModelForm):
	class Meta():
		model = models.Transaction
		fields = ['product', 'count']

class DriverForm(forms.ModelForm):
	class Meta():
		model = models.Driver
		fields = '__all__'