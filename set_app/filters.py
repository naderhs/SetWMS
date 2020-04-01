import django_filters
from set_app.models import *

class ProductFilter(django_filters.FilterSet):
	class Meta:
		model = Product
		fields = '__all__'

