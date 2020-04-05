import django_filters
from set_app.models import *
from django_filters import DateFilter, CharFilter

class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name='timestamp_created',lookup_expr='gte')
	end_date = DateFilter(field_name='timestamp_created',lookup_expr='lte')

	notes = CharFilter(field_name='notes',lookup_expr='icontains')

	class Meta:
		model = Order
		fields = ['id','order_type','driver','permit_type','permit_number','notes','status']
		# exclude = ['warehouse', 'customer', 'timestamp_created']

