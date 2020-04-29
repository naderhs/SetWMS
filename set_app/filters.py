import django_filters
from bootstrap_datepicker_plus import DatePickerInput
from django.forms import DateInput, widgets

from set_app.models import *
from django_filters import DateFilter, CharFilter
import django_filters as filters

class CustomerFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name='created', lookup_expr='gte')
	end_date = DateFilter(field_name='created', lookup_expr='lte')

	first_name = CharFilter(field_name='first_name',lookup_expr='icontains')
	last_name = CharFilter(field_name='last_name',lookup_expr='icontains')
	company_name = CharFilter(field_name='company_name',lookup_expr='icontains')
	melli_code = CharFilter(field_name='melli_code',lookup_expr='icontains')

	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['tel1','tel2','email','address', 'postcode','storage_tags', 'warehouse', 'created']


class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name='created',lookup_expr='gte')
	end_date = DateFilter(field_name='created',lookup_expr='lte')

	notes = CharFilter(field_name='notes',lookup_expr='icontains')

	class Meta:
		model = Order
		fields = ['id','order_type','driver','permit_type','permit_number','notes','status']
		# exclude = ['warehouse', 'customer', 'created']


class InvFilter(django_filters.FilterSet):
	product__code = CharFilter(field_name='product__code', lookup_expr='icontains')
	product__barcode = CharFilter(field_name='product__barcode', lookup_expr='icontains')
	product__name = CharFilter(field_name='product__name', lookup_expr='icontains')
	product__description = CharFilter(field_name='product__description', lookup_expr='icontains')
	product__brand = CharFilter(field_name='product__brand', lookup_expr='icontains')

	class Meta:
		model = Inventory
		fields = ['customer','product','product__code','product__barcode','product__name','product__description','product__brand','product__status']
		# exclude = [inventory__products]


class KardexFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name='created', lookup_expr='gte')
	end_date = DateFilter(field_name='created', lookup_expr='lte')
	order_item__order__id = CharFilter(field_name='order_item__order__id', lookup_expr='icontains')
	invalidated = CharFilter(field_name='invalidated', lookup_expr='icontains')
	order_item__order__permit_number = CharFilter(field_name='order_item__order__permit_number', lookup_expr='icontains')
	product__code = CharFilter(field_name='product__code', lookup_expr='icontains')
	product__barcode = CharFilter(field_name='product__barcode', lookup_expr='icontains')
	product__name = CharFilter(field_name='product__name', lookup_expr='icontains')

	class Meta:
		model = Kardex
		fields = ['customer',
		          'order_item__order__id',
		          'invalidated',
		          'order_item__order__permit_number',
		          'product__code', 'product__barcode',
		          'product__name']
		# widgets = {'created', DateInput()}

