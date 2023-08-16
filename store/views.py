from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
from django.http import HttpResponse
from urllib.parse import unquote
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()  # Corrected 'Product.object' to 'Product.objects'
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):  
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):

    # data = json.loads(request.body.decode('utf-8')) 
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action', action)
    print('productId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
 

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    # return JsonResponse('Item was added', safe=False)
    res = json.dumps({'success': 1,'msg': 'Item was added successfully!!'})
    return HttpResponse(res,content_type='application/json')



def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    else:
        customer, order = guestOrder(request,data)

    total = data['form']['total']
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )


    # below line JsonResponse was in the tutorial
    return JsonResponse('Your Payment Is Complete', safe=False) 
    
    #above line working
    # res = json.dumps({'success': 1,'msg': 'Payment Complete'})
    # return HttpResponse(res,content_type='application/json')
