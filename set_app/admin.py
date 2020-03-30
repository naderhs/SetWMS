from django.contrib import admin
from set_app.models import UserProfileInfo, Warehouse, Customer, Product
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class WarehouseAdmin(admin.ModelAdmin):
	#fields = []
	search_fields = ['name', 'email', 'postcode']
	list_filter = ['name', 'email', 'postcode']
	list_display = ['name', 'email', 'postcode']
	list_editable = ['email', 'postcode']

class ProductAdmin(ImportExportModelAdmin):
	pass

admin.site.register(UserProfileInfo)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)


