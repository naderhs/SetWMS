from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
#from django.core.validators import valid

from django.core.validators import RegexValidator



# Create your models here.

class UserProfileInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.DO_NOTHING)

	# additional
	#portfolio_site = models.URLField(blank=True)

	#profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

	mobile = models.CharField(max_length=11,blank=False,default="09XXXXXXXXX")
	melli_code = models.CharField(max_length=10,blank=False,default="XXXXXXXXXX")

	def __str__(self):
		print("test:")
		return self.user.username


class Warehouse(models.Model):
	name = models.CharField(max_length=256,default="warehouse name")
	tel1 = models.CharField(max_length=256,default="XXXXXXXX")
	tel2 = models.CharField(max_length=256,default="XXXXXXXX")
	email = models.EmailField()
	address = models.CharField(max_length=512,default="address")
	postcode = models.CharField(max_length=10,default="XXXXXXXXXX")

	def __str__(self):
		return self.name + "\n" + self.tel1 + " / " + self.tel2 + " / " + self.email + "\n" + self.address + " " + self.postcode

	def get_absolute_url(self):
		return reverse("set_app:warehouse_detail",kwargs={'pk':self.pk})


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
	first_name = models.CharField(max_length=256,default="first name")
	last_name = models.CharField(max_length=256,default="last name")
	company_name = models.CharField(max_length=256,default="company name")
	tel1 = models.CharField(max_length=256, default="XXXXXXXX")
	tel2 = models.CharField(max_length=256, default="XXXXXXXX")
	email = models.EmailField()
	address = models.CharField(max_length=512,default="address")
	postcode = models.CharField(max_length=10,default="XXXXXXXXXX")
	warehouse = models.ForeignKey(Warehouse,related_name='customers',on_delete=models.CASCADE)

	def __str__(self):
		if self.entity_type == self.INDIVIDUAL:
			return self.entity_type + " - " + self.first_name + " " + self.last_name
		elif self.entity_type == self.COMPANY:
			return self.entity_type + " - " + self.company_name
		else:
			return "Customer __str__ ERROR!"

class Product(models.Model):
	numeric = RegexValidator(r'^[0-9]*$', 'Only anumeric characters are allowed.')

	code= models.CharField(max_length=30,default="product code",blank=False, unique=True)
	barcode = models.CharField(max_length=30,default=0,validators=[numeric])
	name = models.CharField(max_length=128,default="product name",blank=False)
	description = models.CharField(max_length=512, default="some description")
	brand = models.CharField(max_length=128,default="product brand")

	status_choices = (('OFF', 'Off - inactive'), ('ON', 'On - active'))
	status = models.CharField(max_length=20, choices=status_choices, default='ON')

	def __str__(self):
		return self.code + " : " + self.name