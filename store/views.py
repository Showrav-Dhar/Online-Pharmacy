from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
from django.http import HttpResponse
from urllib.parse import unquote
# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()  # Corrected 'Product.object' to 'Product.objects'
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):  # this has some problems , may not work correctly
    # customer = None

    if request.user.is_authenticated:
        # customer, created = Customer.objects.get_or_create(user=request.user)#used gpt
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        # customer, created = Customer.objects.get_or_create(user=request.user)#used gpt
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def updateItem(request):

    data = json.loads(request.body.decode('utf-8')) 
    

    
    productId = data['productId']
    action = data['action']

    print('Action', action)
    print('productId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
 
    # orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    orderItem.save()
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

 

    if orderItem.quantity <= 0:
        orderItem.delete()

    # return JsonResponse('Item was added', safe=False)
    res = json.dumps({'success': 1,'msg': 'Item was added successfully!!'})
    return HttpResponse(res,content_type='application/json')



