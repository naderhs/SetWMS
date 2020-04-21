import django_filters
from bootstrap_datepicker_plus import DatePickerInput
from django.forms import DateInput, widgets

from set_app.models import *
from django_filters import DateFilter, CharFilter
import django_filters as filters

class CustomerFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name='timestamp_created', lookup_expr='gte')
	end_date = DateFilter(field_name='timestamp_created', lookup_expr='lte')

	first_name = CharFilter(field_name='first_name',lookup_expr='icontains')
	last_name = CharFilter(field_name='last_name',lookup_expr='icontains')
	company_name = CharFilter(field_name='company_name',lookup_expr='icontains')
	melli_code = CharFilter(field_name='melli_code',lookup_expr='icontains')

	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['tel1','tel2','email','address', 'postcode','storage_tags', 'warehouse', 'timestamp_created']


class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name='timestamp_created',lookup_expr='gte')
	end_date = DateFilter(field_name='timestamp_created',lookup_expr='lte')

	notes = CharFilter(field_name='notes',lookup_expr='icontains')

	class Meta:
		model = Order
		fields = ['id','order_type','driver','permit_type','permit_number','notes','status']
		# exclude = ['warehouse', 'customer', 'timestamp_created']


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
	# date = filters.DateFromToRangeFilter(field_name='timestamp_created',lookup_expr='gte',
	#                         widget=filters.widgets.RangeWidget(attrs={'class': 'datepicker'}),
	#                                      label='Date Range' )
	# date2 = filters.DateFromToRangeFilter(
	# 	widget=DatePickerInput(format='%m/%d/%Y')
	# )
	# timestamp_created = django_filters.DateTimeFromToRangeFilter(lookup_expr='icontains',
	#                                                       label='Start Date')

	start_date = DateFilter(field_name='timestamp_created', lookup_expr='gte')
	end_date = DateFilter(field_name='timestamp_created', lookup_expr='lte')
	product__code = CharFilter(field_name='product__code', lookup_expr='icontains')
	product__barcode = CharFilter(field_name='product__barcode', lookup_expr='icontains')
	product__name = CharFilter(field_name='product__name', lookup_expr='icontains')
	order__permit_number = CharFilter(field_name='order__permit_number', lookup_expr='icontains')
	order__id = CharFilter(field_name='order__id', lookup_expr='icontains')

	class Meta:
		model = OrderItem
		fields = ['order__customer', 'product__code', 'product__barcode', 'product__name',
		          'order__permit_number', 'order__order_type', 'order__id']
		# widgets = {'timestamp_created', DateInput()}
