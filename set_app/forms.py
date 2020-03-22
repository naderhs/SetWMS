from django import forms
from django.contrib.auth.models import User
from set_app.models import UserProfileInfo
from django.core import validators


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta():
		model = User
		fields = ('first_name','last_name','username','email','password')


class UserProfileInfoForm(forms.ModelForm):
	class Meta():
		model = UserProfileInfo
		fields = ('mobile','melli_code')


class WarehouseForm(forms.Form):
	name = forms.CharField(max_length=30)
	postcode = forms.CharField(max_length=11)
