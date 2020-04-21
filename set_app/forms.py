from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea

from set_app import models
from .widgets import BootstrapDateTimePickerInput

from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta():
		model = User
		fields = '__all__'


class UserProfileInfoForm(forms.ModelForm):
	class Meta():
		model = models.UserProfileInfo
		fields = '__all__'


# class WarehouseForm(forms.Form):
#
# 	def __init__(self, *args, **kwargs):
# 		fields = '__all__'
# 		super(WarehouseForm, self).__init__(*args, **kwargs)
#
# 		self.fields['timestamp_created'] = SplitJalaliDateTimeField(label=_('date time'),
# 		                                                    widget=AdminSplitJalaliDateTime
# 		                                                    # required, for decompress DatetimeField to JalaliDateField and JalaliTimeField
# 		                                                    )


# class CustomerForm(forms.Form):
# 	last_name = forms.CharField(max_length=30)
# 	company_name = forms.CharField(max_length=30)


class OrderForm(forms.ModelForm):
	class Meta():
		model = models.Order
		fields = '__all__'


	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		# self.fields['date'] = JalaliDateField(label=_('date'),  # date format is  "yyyy-mm-dd"
		#                                       widget=AdminJalaliDateWidget  # optional, to use default datepicker
		#                                       )
		#
		# you can added a "class" to this field for use your datepicker!
		# self.fields['date'].widget.attrs.update({'class': 'jalali_date-date'})

		self.fields['timestamp_created'] = SplitJalaliDateTimeField(label='date time',
		                                                    widget=AdminSplitJalaliDateTime
		                                                    # required, for decompress DatetimeField to JalaliDateField and JalaliTimeField
		                                                    )

class ProductForm(forms.ModelForm):
	class Meta():
		model = models.Product
		fields = '__all__'
		widgets = {
			'notes': Textarea(attrs={'cols': 200, 'rows': 5}),
		}


class OrderItemForm(forms.ModelForm):
	class Meta():
		model = models.OrderItem
		fields = ['product', 'count']


class DriverForm(forms.ModelForm):
	class Meta():
		model = models.Driver
		fields = '__all__'

class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=BootstrapDateTimePickerInput()
    )