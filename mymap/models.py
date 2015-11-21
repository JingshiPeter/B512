from django.db import models


# Create your models here.
class Customer(models.Model):
	#id = models.AutoField(primary_key=True) Django default primary key
	name = models.CharField(max_length=50, null=False, unique=True)
	streetnumber = models.IntegerField(null=True, default=0)
	streetname = models.CharField(max_length=20,blank=True, null=True)
	zipcode = models.IntegerField(null=True, default=0)
	city = models.CharField(max_length=20, blank=True, default='Austin')
	state = models.CharField(max_length=2, blank=True, default='TX')
	owner = models.ForeignKey('auth.User', related_name='customers')
	def __unicode__(self):
		return str(self.name)

class Order(models.Model):
	customer = models.ForeignKey('Customer',related_name='orders')
	date = models.DateField()
	quantity = models.IntegerField()
	timewindows1 = models.IntegerField(default=9)
	timewindowe1 = models.IntegerField(default=18)
	timewindows2 = models.IntegerField(default=18)
	timewindowe2 = models.IntegerField(default=9)
