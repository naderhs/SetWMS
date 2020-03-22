from django.db import models
from django.contrib.auth.models import User


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
