from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from django.core.validators import valid
from django.core.exceptions import ValidationError

from django.core.validators import RegexValidator
import re

DEFAULT_WH_ID = 1
NUMERIC = RegexValidator(r'^[0-9]*$', 'Only anumeric characters are allowed.')


# Create your models here.

class UserProfileInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

	# additional
	# portfolio_site = models.URLField(blank=True)

	# profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

	mobile = models.CharField(max_length=11, blank=False, default="09XXXXXXXXX")
	melli_code = models.CharField(max_length=10, blank=False, default="XXXXXXXXXX")

	def clean(self):
		super().clean()
		if not MelliCodeIsValid(self.melli_code):
			raise ValidationError('Melli code is invalid!')

	def __str__(self):
		return self.user.username


class Warehouse(models.Model):
	name = models.CharField(max_length=256, default="warehouse name")
	tel1 = models.CharField(max_length=256, default="XXXXXXXX")
	tel2 = models.CharField(max_length=256, default="XXXXXXXX")
	email = models.EmailField()
	address = models.CharField(max_length=512, default="address")
	postcode = models.CharField(max_length=10, default="XXXXXXXXXX")
	timestamp_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("set_app:warehouse_detail", kwargs={'pk': self.pk})


class StorageTag(models.Model):
	name = models.CharField(max_length=256, default="Storage Tag Name")

	def __str__(self):
		return self.name


class Customer(models.Model):
	INDIVIDUAL = 'IN'
	COMPANY = 'CO'
	OTHER = 'OT'

	ENTITY_TYPE_CHOICES = [
		(INDIVIDUAL, 'Individual'),
		(COMPANY, 'Company'),
		(OTHER, 'Other'),
	]
	entity_type = models.CharField(
		max_length=2,
		choices=ENTITY_TYPE_CHOICES,
		default=INDIVIDUAL,
	)
	first_name = models.CharField(max_length=256, default="first name", blank=True)
	last_name = models.CharField(max_length=256, default="last name", blank=True)
	company_name = models.CharField(max_length=256, default="company name", blank=True)
	melli_code = models.CharField(max_length=10, default=0, validators=[NUMERIC])
	tel1 = models.CharField(max_length=256, default="XXXXXXXX")
	tel2 = models.CharField(max_length=256, default="XXXXXXXX", blank=True)
	email = models.EmailField()
	address = models.CharField(max_length=512, default="address")
	postcode = models.CharField(max_length=10, default="XXXXXXXXXX")
	storage_tags = models.ManyToManyField(StorageTag)
	timestamp_created = models.DateTimeField(auto_now_add=True)
	warehouse = models.ForeignKey(Warehouse, related_name='customers', on_delete=models.CASCADE, default=DEFAULT_WH_ID)

	def clean(self):
		super().clean()
		if self.entity_type == self.INDIVIDUAL:
			if len(self.first_name) == 0 or len(self.last_name) == 0:
				raise ValidationError('first_name and last_name cannot be empty!', code='invalid')
		elif self.entity_type == self.COMPANY:
			if len(self.company_name) == 0:
				raise ValidationError('company_name cannot be empty!')
		elif not MelliCodeIsValid(self.melli_code):
			raise ValidationError('Melli code is invalid!')

	def __str__(self):
		if self.entity_type == self.INDIVIDUAL:
			return self.entity_type + " - " + self.first_name + " " + self.last_name
		elif self.entity_type == self.COMPANY:
			return self.entity_type + " - " + self.company_name
		else:
			return "Customer __str__ ERROR!"


class Product(models.Model):
	code = models.CharField(max_length=30, default="product code", blank=False, unique=True)
	barcode = models.CharField(max_length=30, default=0, validators=[NUMERIC])
	name = models.CharField(max_length=128, default="product name", blank=False)
	description = models.CharField(max_length=512, default="some description", blank=True)
	brand = models.CharField(max_length=128, default="product brand")
	timestamp_created = models.DateTimeField(auto_now_add=True)
	status_choices = (('OFF', 'Off - inactive'), ('ON', 'On - active'))
	status = models.CharField(max_length=20, choices=status_choices, default='ON')

	def __str__(self):
		return self.code + " : " + self.name

class Driver(models.Model):
	melli_code = models.CharField(max_length=10, default=0, validators=[NUMERIC])
	first_name = models.CharField(max_length=256, default="first name", blank=True)
	last_name = models.CharField(max_length=256, default="last name", blank=True)
	driver_code = models.CharField(max_length=20, default=0, validators=[NUMERIC])
	tel1 = models.CharField(max_length=256, default="XXXXXXXX")
	number_plate_1 = models.CharField(max_length=3, default=000, validators=[NUMERIC])
	persian_letters = (
		('الف', 'الف'), ('ب', 'ب'), ('پ', 'پ'), ('ت', 'ت'), ('ث', 'ث'),
		('ج', 'ج'), ('چ', 'چ'), ('ح', 'ح'), ('خ', 'خ'), ('د', 'د'),
		('ذ', 'ذ'), ('ر', 'ر'), ('ز', 'ز'), ('ژ', 'ژ'), ('س', 'س'),
		('ش', 'ش'), ('ص', 'ص'), ('ض', 'ض'), ('ط', 'ط'), ('ظ', 'ظ'),
		('ع', 'ع'), ('غ', 'غ'), ('ف', 'ف'), ('ک', 'ک'), ('گ', 'گ'),
		('ل', 'ل'), ('م', 'م'), ('ن', 'ن'), ('و', 'و'), ('ه', 'ه'),
		('ی', 'ی'))

	number_plate_letter = models.CharField(max_length=3, default='الف', choices=persian_letters)
	number_plate_2 = models.CharField(max_length=2, default=00, validators=[NUMERIC])
	number_plate_iran = models.CharField(max_length=2, default=00, validators=[NUMERIC])

	truck_sizes = (
		('MOT', 'Motorbike - موتور'),
		('CAR', 'Car - سواری'), ('VAN', 'Vanet peykan - وانت پیکان'), ('NIS', 'Nissan - نیسان'),
		('ISU', 'ISUZU - ایسوزو'), ('KHA', 'KHAVAR - خاور'), ('BUD', 'BUDSAN - بادسان'),
		('TAK', 'TAK - تک'), ('JOF', 'JOFT - جفت'), ('20F', '20 Foot container - کانتینر ۲۰ فوت'),
		('40F', '40 Foot container - کانتینر ۴۰ فوت'), ('40H', '40 Foot HIGH container  - کانتینر ۴۰ فوت های'),
		('FBT', 'Flat bed trailer - تریلی کفی'),
		('SRT', 'Side raised trailer - تریلی بغلدار'), ('TRT', 'Transit trailer  - تریلی ترانزیتی')
	)
	truck_size = models.CharField(max_length=100, choices=truck_sizes, default='ON')
	timestamp_created = models.DateTimeField(auto_now_add=True)

	def clean(self):
		super().clean()
		if not MelliCodeIsValid(self.melli_code):
			raise ValidationError('Melli code is invalid!')

	def __str__(self):
		return self.first_name + " " + self.last_name


class Order(models.Model):
	sys_order_no = models.PositiveIntegerField()
	warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, default=DEFAULT_WH_ID)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
	# customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order_choices = (('IN', 'Inbound'), ('OU', 'Outbound'), ('TR', 'Transfer '))
	order_type = models.CharField(max_length=10, choices=order_choices, default='ON', null=False)
	permit_choices = (('PAP', 'Paper'), ('FAX', 'Fax'), ('EMA', 'Email'), ('TEL', 'Telephone'))
	permit_type = models.CharField(max_length=10, choices=permit_choices, default='ON', null=False)
	permit_number = models.CharField(max_length=30, default="0", blank=False, unique=False, null=True)
	notes = models.TextField(max_length=2048, default="some notes", blank=True)
	origin_destination = models.CharField(max_length=30, default="0", blank=False, null=True)
	billway_number = models.CharField(max_length=30, default="0", blank=False, unique=False, null=True)
	transport_company = models.CharField(max_length=256, default="company name", blank=True)
	sender_receiver = models.CharField(max_length=50, default="0", blank=False, unique=False, null=True)
	receiving_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='receiving_customer') #used only for transfer
	status_choices = (('OFF', 'Off - inactive'), ('ON', 'On - active'))
	status = models.CharField(max_length=20, choices=status_choices, default='ON')
	timestamp_created = models.DateTimeField(auto_now_add=True)
	driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)


	def __str__(self):
		return self.order_type + " : " + self.customer.__str__() + " : " + self.status + " <" + self.timestamp_created.__str__() + ">"


class Transaction(models.Model):

	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	count = models.IntegerField(default=0, null=False)
	timestamp_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.order.__str__() + " : " + self.product.__str__() + " <" + self.count.__str__() + ">"




def MelliCodeIsValid(input):
	if not re.search(r'^\d{10}$', input):
		return False
	check = int(input[9])
	s = sum([int(input[x]) * (10 - x) for x in range(9)]) % 11
	return (s < 2 and check == s) or (s >= 2 and check + s == 11)
