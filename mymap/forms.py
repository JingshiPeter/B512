from django.forms import ModelForm
from mymap.models import Customer, Order

class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = ['name','streetname','streetnumber','zipcode','city','state','owner']

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['customer','date','quantity','timewindows1','timewindowe1','timewindows2','timewindowe2']