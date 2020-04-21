from django.contrib import admin
from set_app.models import *
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class WarehouseAdmin(admin.ModelAdmin):
	# fields = []
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
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(StorageTag)
admin.site.register(Driver)

# from django.utils.translation import gettext_lazy as _
# from SetWMS.apps.core import get_multilingual_field_names
# from .models import Idea
#
#
# @admin.register(Idea)
# class IdeaAdmin(admin.ModelAdmin):
# 	fieldsets = [
# 		(_("Title and Content"), {
# 			"fields": get_multilingual_field_names("title") + get_multilingual_field_names("content")
# 		}),
# 	]
