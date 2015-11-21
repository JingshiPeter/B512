from django.shortcuts import render
from .models import Customer, Order
from django.http import HttpResponseRedirect
from .forms import CustomerForm, OrderForm
from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view
from django.core import serializers

# import mymap.generate_edges
#RESTful API
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from mymap.models import Customer, Order
from mymap.permissions import IsOwnerOrReadOnly
from mymap.serializers import CustomerSerializer, UserSerializer, OrderSerializer

class CustomerViewSet(viewsets.ModelViewSet):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
	def perform_create(self, serializer):
		serializer.save(owner=User.objects.get(id = self.request.POST.get('owner')))
		# serializer.save(owner=self.request.POST.get('owner'))
		# serializer.save(owner_id=self.request.POST.get('owner'))
		# serializer.save()

class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
	def perform_create(self, serializer):
		serializer.save(customer = Customer.objects.get(id = self.request.POST.get('customer')))
    
class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

def calc(request):
	day_orders = Order.objects.filter(date="2015-11-16")
	addresses = []
	addresses.append("407 Radam Ln") #Depot, (512) Brewery
	for order in day_orders:
		address = ""
		address = address + str(order.customer.streetnumber)
		address += " "
		address += str(order.customer.streetname)
		address += " Austin TX"
		addresses.append(address)
	# addresses = mymap.generate_edges.test_addresses()
	return render(request, "calc.html",{'addresses' : addresses})

def testing(request):
	form = CustomerForm()
	form1 = CustomerForm()
	form2 = OrderForm()
	if(request.method == 'POST'):
		# name,state = (request.POST)
		form1 = CustomerForm(request.POST)
		# if form.is_valid():
		# 	form.save()
		return render(request, "testing.html",{'reply' : 'Yo','form' : form,'form1' : form1,'form2' : form2})
	else:
		return render(request, "testing.html",{'reply' : 'Bad','form' : form,'form1' : form1,'form2' : form2})

def home(request):
	return render(request, "home.html",{})
def contact(request):
	return render(request, "contact.html",{})
def about(request):
	return render(request, "about.html",{})
def thanks(request):
	return render(request, "thanks.html",{})
def map(request):
	return render(request, "map.html",{})


def order(request):
	form = OrderForm();
	return render(request, "order.html",{"form": form})


#this view is for savecustomerform ajax
@json_view
def savecustomerform(request): 
	form = CustomerForm(request.POST or None)
	if form.is_valid():
		form.save()
		name = form.cleaned_data['name']
		streetnumber = form.cleaned_data['streetnumber']
		streetname = form.cleaned_data['streetname']
		zipcode = form.cleaned_data['zipcode']
		city = form.cleaned_data['city']
		state = form.cleaned_data['state']
		owner = form.cleaned_data['owner']
		customer = Customer(name = name, streetnumber = streetnumber, streetname = streetname, zipcode = zipcode, city = city, state=state,owner = owner)
		customer.save()
		return {'success': True}
	else:
		# RequestContext ensures CSRF token is placed in newly rendered form_html
	    request_context = RequestContext(request)
	    form_html = render_crispy_form(form, context=request_context)
	    return {'success': False, 'form_html': form_html}


def showcustomers(request):


	# Customer_list = serializers.serialize("json", customers.objects.all())
	customer_list = Customer.objects.all()

	context = {
		"customer_list" : customer_list,
		"length" : len(customer_list),
	}
	return render(request, "showcustomers.html",context)

# def db(request):

#     greeting = Greetings()
#     greeting.save()

#     greetings = Greetings.objects.all()

#     return render(request, 'db.html', {'greetings': greetings})

def customer(request):
	form = CustomerForm()
	return render(request, 'customer.html', {'form' : form})

# @json_view
# def save_Customer_form(request):
#     form = ExampleForm(request.POST or None)
#     if form.is_valid():
#         # You could actually save through AJAX and return a success code here
#         form.save()
#         return {'success': True}

#     # RequestContext ensures CSRF token is placed in newly rendered form_html
#     request_context = RequestContext(request)
#     form_html = render_crispy_form(form, context=request_context)
#     return {'success': False, 'form_html': form_html}