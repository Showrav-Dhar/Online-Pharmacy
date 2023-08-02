from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

# Create your views here.

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action', action)
    print('productId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)  # Fixed 'product' to 'Product'
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    try:
        orderItem = OrderItem.objects.get(order=order, product=product)
        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1
            if orderItem.quantity <= 0:
                orderItem.delete()
        orderItem.save()
    except OrderItem.DoesNotExist:
        if action == 'add':
            orderItem = OrderItem.objects.create(order=order, product=product, quantity=1)
    
    return JsonResponse('Item was added', safe=False)
