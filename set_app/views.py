import csv

from django.contrib import messages
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm

from set_app.forms import *
from set_app.models import *
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from set_app.filters import *
from django.forms import inlineformset_factory

# Imports for PDF to work
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

# Create your views here.
def index(request):
	return render(request, 'set_app/index.html')

# Dashboard view
@login_required(login_url='set_app:user_login')
def dashboard(request):
	customers = Customer.objects.all()
	total_customers = customers.count()

	orders = Order.objects.all()
	total_orders = orders.count()

	# Total customer, Total served last month, this month to today, last week, yesterday, today
	# Total orders, Total served last month, this month to today, last week, yesterday, today
	# Total units, Total units last month, this month to today, last week, yesterday, today

	context = {'customers':customers,'orders':orders,'total_customers':total_customers,'total_orders':total_orders}
	return render(request, 'set_app/dashboard/dashboard.html', context)

@login_required(login_url='set_app:user_login')
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('set_app:user_login'))

def special(request):
	return HttpResponse('You are logged in nice!')

def register(request):
	registered = False
	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileInfoForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'profile_pic' in request.FILES:
				profile.profile_pic = request.FILES['profiles_pic']

			profile.save()

			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileInfoForm()

	return render(request, 'set_app/registration.html',
	              {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('set_app:dashboard'))

			else:
				print('======= Account is inactive!')
				messages.info(request, 'Account is inactive!')
				return render(request, 'set_app/login.html', {})
				# return HttpResponse('ACCOUNT NOT ACTIVE')
		else:
			print('======= Username or password is incorrect!')
			messages.info(request, 'Username or password is incorrect!')
			return render(request, 'set_app/login.html', {})
	else:
		return render(request, 'set_app/login.html', {})

class WarehouseListView(ListView):
	template_name = 'set_app/warehouse/warehouse_list.html'
	context_object_name = 'warehouses'
	model = Warehouse

class WarehouseDetailView(DetailView):
	context_object_name = 'warehouse_detail'
	model = Warehouse
	template_name = 'set_app/warehouse/warehouse_detail.html'

class WarehouseCreateView(CreateView):
	template_name = 'set_app/warehouse/warehouse_form.html'
	fields = ('name', 'tel1', 'tel2', 'email', 'address', 'postcode')
	model = Warehouse

class WarehouseUpdateView(UpdateView):
	template_name = 'set_app/warehouse/warehouse_form.html'
	fields = ('name', 'tel1', 'tel2', 'email', 'address', 'postcode')
	model = Warehouse

class WarehouseDeleteView(DeleteView):
	template_name = 'set_app/warehouse/warehouse_form.html'
	model = Warehouse
	success_url = reverse_lazy("set_app:warehouse_list")


# Customer Views
def CustomerListView(request):
	customers = Customer.objects.all()
	cust_filter = CustomerFilter(request.GET, queryset=customers)
	customers = cust_filter.qs

	context = {'customers': customers, 'cust_filter': cust_filter}
	return render(request, 'set_app/customer/customer_list.html', context)


def CustomerMorDetailView(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.orders.all()
	total_orders = orders.count()
	customer_name = customer.__str__

	myFilter = OrderFilter(request.GET,queryset=orders)
	orders = myFilter.qs

	context = {'customer':customer, 'orders':orders, 'total_orders':total_orders, 'customer_name':customer_name,'myfilter':myFilter}
	return render(request, 'set_app/customer/customer_more_detail.html', context)

class CustomerDetailView(DetailView):
	template_name = 'set_app/customer/customer_detail.html'
	context_object_name = 'customer_detail'
	model = Customer

class CustomerCreateView(CreateView):
	template_name = 'set_app/customer/customer_form.html'
	fields = ('entity_type', 'first_name', 'last_name', 'company_name', 'tel1', 'tel2', 'email', 'address', 'postcode', 'warehouse')
	model = Customer
	success_url = reverse_lazy("set_app:dashboard")

class CustomerUpdateView(UpdateView):
	template_name = 'set_app/customer/customer_form.html'
	fields = ('entity_type', 'first_name', 'last_name', 'company_name', 'tel1', 'tel2', 'email', 'address', 'postcode', 'warehouse')
	model = Customer
	success_url = reverse_lazy("set_app:customer_list")

class CustomerDeleteView(DeleteView):
	template_name = 'set_app/customer/customer_form.html'
	model = Customer
	success_url = reverse_lazy("set_app:customer_list")

# Order Views
def OrderCreateView(request, pk=-1, ot='IN'):
	WH_ID = 1
	if pk > 0:
		customer = Customer.objects.get(id=pk)
		order_form = OrderForm(initial={'warehouse_id':WH_ID, 'customer': customer,'order_type':ot})
	else:
		order_form = OrderForm(initial={'warehouse_id':WH_ID,'order_type':ot})

	TransactionFormSet = inlineformset_factory(Order, Transaction, fields=['product', 'count'],extra=5)
	formset = TransactionFormSet()

	driver_form = DriverForm()
	print("Before request.method == 'POST' ===== ")
	if request.method == 'POST':
		data = request.POST.copy()
		data['warehouse'] = 1
		data['sys_order_no'] = 999
		data['order_type'] = ot
		order_form = OrderForm(data)
		driver_form = DriverForm(request.POST)
		print("Before order_form.is_valid() ===== " + order_form.is_valid().__str__())
		if order_form.is_valid():
			print("Inside order_form.is_valid() ===== ")
			order = order_form.save(False)
			if ot != 'TR' and driver_form.is_valid():
				driver = driver_form.save()
				order.driver=driver
			if ot != 'TR':
				print("driver_form.errors > " + driver_form.errors.__str__())
				print("driver_form.non_field_errors > " + driver_form.non_field_errors.__str__())
			order.save()
			formset = TransactionFormSet(request.POST, instance=order)
			print("formset.is_valid(): "+ formset.is_valid().__str__())
			if formset.is_valid():
				print(" inside formset.is_valid() ===== ")
				formset.save()
				return redirect('set_app:dashboard')
		else:
			pass
			print("request.POST > " + request.POST.__str__())
			print("order_form.errors > " + order_form.errors.__str__())
			print("order_form.non_field_errors > " + order_form.non_field_errors.__str__())
	context = {'order_form':order_form, 'driver_form':driver_form, 'formset':formset}
	return render(request, 'set_app/order/order_form.html', context)

# class ProductListView(ListView):
# 	context_object_name = 'items'
# 	model = Product
#
# 	def get_context_data(self, **kwargs):
# 		context = super(ProductListView, self).get_context_data(**kwargs)
# 		context['header'] = 'all products'
# 		items = Product.objects.all()
# 		context['items'] = items
# 		return context
#
# 	def get_queryset(self):
# 		qs = self.model.objects.all()
# 		product_filtered_list = ProductFilter(self.request.GET, queryset=qs)
# 		return product_filtered_list.qs

def ProductListView(request):
	products = Product.objects.all()
	return render(request, 'set_app/product/product_list.html', {'items':products, 'header': 'all products'})


def ActiveProductsView(request):
	items = Product.objects.filter(status='ON')
	context = {
		'items': items,
		'header': 'active products'
	}
	return render(request, 'set_app/product/product_list.html', context)

def ProductCreateView(request):
	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('set_app:product_list')
	else:
		product_form = ProductForm()
	return render(request, 'set_app/product/product_form.html', {'product_form':product_form})

def ProductUpdateView(request, pk):
	item = get_object_or_404(Product, pk=pk)
	if request.method == 'POST':
		product_form = ProductForm(request.POST, instance=item)
		if product_form.is_valid():
			product_form.save()
			return redirect('set_app:product_list')
	else:
		product_form = ProductForm(instance=item)
	return render(request, 'set_app/product/product_form.html', {'product_form':product_form})

def ProductDeleteView(request, pk):
	Product.objects.filter(id=pk).delete()
	items = Product.objects.all()
	context = {
		'items':items
	}
	return redirect('set_app:product_list')


# Driver
# def DriverListView(request):
# 	drivers = Product.objects.all()
# 	return render(request, 'set_app/product_list.html',{'items':products, 'header':'all products'})

class DriverCreateView(CreateView):
	fields = ('melli_code','first_name','last_name','transport_company','driver_code','tel1','number_plate_1','number_plate_letter','number_plate_2','number_plate_iran','truck_size')
	model = Driver
	success_url = reverse_lazy("set_app:driver_create")


#Reports
def InventoryView(request):
	inv = Inventory.objects.all()
	inv_filter = InvFilter(request.GET, queryset=inv)
	inv = inv_filter.qs
	context = {'inv': inv, 'inv_filter': inv_filter}
	if request.method == 'POST':
		print("Entered POST")
		print(inv.__str__())
		print(inv.__len__())
		response = HttpResponse(content_type='text/csv')
		writer = csv.writer(response)
		writer.writerow(['#', 'Customer', 'Product code', 'Product barcode', 'Product name', 'Product description',
		                 'Product brand', 'Product status', 'Count'])
		for idx, item in enumerate(inv):
			writer.writerow([idx+1, item.customer,item.product.code, item.product.barcode,item.product.name,
			                item.product.description,item.product.brand,item.product.status,item.count])
		response['Content-Disposition'] = 'attachment; filename="inventory.csv"'
		return response
	return render(request, 'set_app/reports/inv_report.html', context)

# def InventoryCsvExport(request):
# 	print(request.POST)
# 	response = HttpResponse(content_type='text/csv')
# 	writer = csv.writer(response)
# 	writer.writerow(['#', 'Customer', 'Product code', 'Product barcode', 'Product name', 'Product description',
# 	                 'Product brand', 'Product status', 'Count'])
# 	# for i in items.objects.all().value_list('customr','product'):
# 	# 	writer.writerow(i)
#
# 	response['Content-Disposition'] = 'attachment; filename="inventory.csv"'
# 	return response
#
# # PDF code stats here
# def render_to_pdf(template_src, context_dict={}):
# 	template = get_template(template_src)
# 	html = template.render(context_dict)
# 	result = BytesIO()
# 	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
# 	if not pdf.err:
# 		return HttpResponse(result.getvalue(), content_type='application/pdf')
# 	return None
#
# data = {
# 	"company": "Dennnis Ivanov Company",
# 	"address": "123 Street name",
# 	"city": "Vancouver",
# 	"state": "WA",
# 	"zipcode": "98663",
#
# 	"phone": "555-555-2345",
# 	"email": "youremail@dennisivy.com",
# 	"website": "dennisivy.com",
# }
#
#
# # Opens up page as PDF
# class CustomerViewPDF(View):
# 	def get(self, request, *args, **kwargs):
# 		pdf = render_to_pdf('set_app/customer_pdf_template.html', data)
# 		return HttpResponse(pdf, content_type='application/pdf')
#
#
# # Automaticly downloads to PDF file
# class CustomerDownloadPDF(View):
# 	def get(self, request, *args, **kwargs):
# 		pdf = render_to_pdf('set_app/customer_pdf_template.html', data)
#
# 		response = HttpResponse(pdf, content_type='application/pdf')
# 		filename = "Invoice_%s.pdf" % ("12341231")
# 		content = "attachment; filename=%s" % (filename)
# 		response['Content-Disposition'] = content
# 		return response

