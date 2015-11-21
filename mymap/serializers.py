from rest_framework import serializers
from django.contrib.auth.models import User
from mymap.models import Customer, Order

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    owner= serializers.ReadOnlyField(source='owner.username')
    owner_id= serializers.ReadOnlyField(source='owner.id')
    # owner= serializers.ReadOnlyField()
    orders = serializers.HyperlinkedRelatedField(queryset=Order.objects.all(), view_name='order-detail', many=True)
    # highlight = serializers.HyperlinkedIdentityField(view_name='customer-highlight', format='html')
    
    class Meta:
        model = Customer
        fields = ('url','owner_id','id','owner','name', 'streetnumber', 'streetname',
                  'city', 'state', 'zipcode','orders')
                  
class UserSerializer(serializers.HyperlinkedModelSerializer):
    customers = serializers.HyperlinkedRelatedField(queryset=Customer.objects.all(), view_name='customer-detail', many=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'customers')

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.name')
    customer_id = serializers.ReadOnlyField(source='customer.id')
    # highlight = serializers.HyperlinkedIdentityField(view_name='customer-highlight', format='html')
    
    class Meta:
        model = Order
        fields = ('url','customer_id','customer','date','quantity','timewindows1','timewindowe1','timewindows2','timewindowe2')