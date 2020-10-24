from django.shortcuts import render
from django.http import JsonResponse
from . models import *
import json
from django.views.generic import TemplateView, ListView
from django.db.models import Q
import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

def home(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		trayItems = order.get_tray_items
	else:
		items = []
		order = {'get_tray_total': 0, 'get_total': 0}
		trayItems = order['get_tray_total']

	object_list = Food.objects.all().order_by('name')
	paginator = Paginator(object_list, 6)
	page = request.GET.get('page')
	food_list = paginator.get_page(page)
	context = {'food_list': food_list, 'trayItems': trayItems}
	return render(request, 'hotel/home.html', context)


@login_required
def tray(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		trayItems = order.get_tray_items
	else:
		items = []
		order = {'get_tray_total': 0, 'get_total': 0}
		trayItems = order['get_tray_total'] 

	context = {'items': items, 'order': order, 'trayItems': trayItems}
	return render(request, 'hotel/tray.html', context)


@login_required
def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		if not ShippingAddress.objects.filter(customer=customer): 
			delivery = {'address':'', 'city':'', 'phone_number':''}
		else:
			delivery = ShippingAddress.objects.get(customer=customer)
		items = order.orderitem_set.all()
		trayItems = order.get_tray_items
	else:
		items = []
		order = {'get_tray_total': 0, 'get_total': 0}
		trayItems = order['get_tray_total']
	
	context = {'items': items, 'order': order, 'trayItems': trayItems, 'delivery': delivery}

	return render(request, 'hotel/checkout.html', context)


def updateTray(request):
	data = json.loads(request.body)
	productID = data['productID']
	action = data['action']
	customer = request.user.customer
	food = Food.objects.get(id=productID)
	order, created = Order.objects.get_or_create(customer=customer,complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=food)
	if action == 'Add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'Remove':
		orderItem.quantity = (orderItem.quantity - 1)
	
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item Was Added', safe=False)  


def search_results(request):
	query = request.GET.get('Search')
	results = Food.objects.filter(Q(name__icontains=query)).order_by('name')
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		trayItems = order.get_tray_items
	else:
		items = []
		order = {'get_tray_total': 0, 'get_total': 0}
		trayItems = order['get_tray_total']


	# object_list = Food.objects.all().order_by('name')
	paginator = Paginator(results, 6)
	page = request.GET.get('page')
	result_list = paginator.get_page(page)
	context = {'result_list': result_list, 'trayItems': trayItems}
	return render(request, 'hotel/search_results.html', context)	

def processOrder(request):
	data = json.loads(request.body)
	transaction_id = datetime.datetime.now().timestamp()
	if request.user.is_authenticated:
		customer = request.user.customer
		name = data['userData']['name']
		email = data['userData']['email']
		address = data['deliveryData']['address']
		city = data['deliveryData']['city']
		phone_number = data['deliveryData']['phoneNumber']
		customer_order = Order.objects.get(customer=customer,complete=False)
		delivery, created = ShippingAddress.objects.get_or_create(customer = customer,
																	phone_number = phone_number,
																	address = address,
																	city=city)
		cost = customer_order.get_tray_total
		response = f"Order has been processed, details are as follows: \n transaction id: {transaction_id} \n customer: {name} \n email: {email} \n address: {address} \n city: {city} \n Contact: {phone_number} \n TOTAL: {cost}"

		customer_order.transaction_id = str(transaction_id)
		customer_order.complete = True
		customer_order.save()
	else:
		response = "User is not Logged In..."	
	return JsonResponse(response, safe=False)
