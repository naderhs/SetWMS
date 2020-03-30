from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from set_app.forms import UserForm, UserProfileInfoForm, ProductForm
from set_app import models
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404


# Imports for PDF to work
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

# Create your views here.
def index(request):
	return render(request, 'set_app/index.html')


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

@login_required
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
				return HttpResponseRedirect(reverse('index'))

			else:
				return HttpResponse('ACCOUNT NOT ACTIVE')
		else:
			print('someone tried to login and failed')
			print('uusername: {} and password {}'.format(username, password))
			return HttpResponse("invalid login details supplied! ")
	else:
		return render(request, 'set_app/login.html', {})


class WarehouseListView(ListView):
	context_object_name = 'warehouses'
	model = models.Warehouse

class WarehouseDetailView(DetailView):
	context_object_name = 'warehouse_detail'
	model = models.Warehouse
	template_name = 'set_app/warehouse_detail.html'

class WarehouseCreateView(CreateView):
	fields = ('name', 'tel1', 'tel2', 'email', 'address', 'postcode')
	model = models.Warehouse

class WarehouseUpdateView(UpdateView):
	fields = ('name', 'tel1', 'tel2', 'email', 'address', 'postcode')
	model = models.Warehouse

class WarehouseDeleteView(DeleteView):
	model = models.Warehouse
	success_url = reverse_lazy("set_app:warehouse_list")


# Customer Views
class CustomerListView(ListView):
	context_object_name = 'customers'
	model = models.Customer

class CustomerDetailView(DetailView):
	context_object_name = 'customer_detail'
	model = models.Customer
	template_name = 'set_app/customer_detail.html'

class CustomerCreateView(CreateView):
	fields = ('entity_type', 'first_name', 'last_name', 'company_name', 'tel1', 'tel2', 'email', 'address', 'postcode', 'warehouse')
	model = models.Customer
	success_url = reverse_lazy("set_app:customer_list")

class CustomerUpdateView(UpdateView):
	fields = ('entity_type', 'first_name', 'last_name', 'company_name', 'tel1', 'tel2', 'email', 'address', 'postcode', 'warehouse')
	model = models.Customer
	success_url = reverse_lazy("set_app:customer_list")

class CustomerDeleteView(DeleteView):
	model = models.Customer
	success_url = reverse_lazy("set_app:customer_list")

# Product Views
class ProductListView(ListView):
	context_object_name = 'products'
	model = models.Product

	def get_context_data(self, **kwargs):
		context = super(ProductListView, self).get_context_data(**kwargs)
		context['header'] = 'all products'
		context['items'] = models.Product.objects.all()
		return context

def ActiveProductsView(request):
	items = models.Product.objects.filter(status='ON')
	context = {
		'items': items,
		'header': 'active products'
	}
	return render(request, 'set_app/product_list.html', context)

def ProductCreateView(request):
	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('set_app:product_list')
	else:
		product_form = ProductForm()
	return render(request, 'set_app/product_form.html', {'product_form':product_form})

def ProductUpdateView(request, pk):
	item = get_object_or_404(models.Product, pk=pk)
	if request.method == 'POST':
		product_form = ProductForm(request.POST, instance=item)
		if product_form.is_valid():
			product_form.save()
			return redirect('set_app:product_list')
	else:
		product_form = ProductForm(instance=item)
	return render(request, 'set_app/product_form.html', {'product_form':product_form})

def ProductDeleteView(request, pk):
	models.Product.objects.filter(id=pk).delete()
	items = models.Product.objects.all()
	context = {
		'items':items
	}
	return redirect('set_app:product_list')


# PDF code stats here
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

data = {
	"company": "Dennnis Ivanov Company",
	"address": "123 Street name",
	"city": "Vancouver",
	"state": "WA",
	"zipcode": "98663",

	"phone": "555-555-2345",
	"email": "youremail@dennisivy.com",
	"website": "dennisivy.com",
}


# Opens up page as PDF
class CustomerViewPDF(View):
	def get(self, request, *args, **kwargs):
		pdf = render_to_pdf('set_app/customer_pdf_template.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class CustomerDownloadPDF(View):
	def get(self, request, *args, **kwargs):
		pdf = render_to_pdf('set_app/customer_pdf_template.html', data)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Invoice_%s.pdf" % ("12341231")
		content = "attachment; filename=%s" % (filename)
		response['Content-Disposition'] = content
		return response

