from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
from django.http import HttpResponse
from urllib.parse import unquote
import datetime
from .utils import cookieCart,cartData

# Create your views here.

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()  # Corrected 'Product.object' to 'Product.objects'
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def healthtips(request):#added by showrav
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'data': data, 'cartItems': cartItems}

    return render(request, 'store/healthtips.html', context)



def items_view(request):
    # Your view logic goes here
    return render(request, 'store/#items/.html')  # Verify the template path



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

    res = json.dumps({'success': 1,'msg': 'Item was added successfully!!','action':action})
    return HttpResponse(res,content_type='application/json')



def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    else:#guest user start 
        #did not use the custom util function
        print('User Not Logged In..')
    
        print('COOKIES: ', request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']

        cookieData = cookieCart(request)
        items = cookieData['items']

        customer, created = Customer.objects.get_or_create(
            email = email,
        )
        customer.name = name
        customer.save()


        order = Order.objects.create(
            customer = customer,
            complete = False
        )

        for item in items:
            product = Product.objects.get(id = item['product']['id'])

            orderItem = OrderItem.objects.create(
                product = product,
                order = order,
                quantity = item['quantity']
            )
    #guest user end

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

    return JsonResponse('Payment Completed', safe=False) 
    

# 55.03

def fetch_products(request,category_id):
    if category_id == "all":
        products = Product.objects.select_related('category').all()
    else:
        # products = Product.objects.get(category_id=category_id)
        products = Product.objects.filter(category_id=category_id)
    product_list = [{'id': product.id,'name': product.name, 'price': product.price,'imageURL': product.imageURL,'category': product.category.name} for product in products]
    return JsonResponse({'products': product_list})

def fetch_category(request):
    categories = Category.objects.all()
    category_list = [{'name': category.name,'id' : category.id} for category in categories]
    return JsonResponse({'categories': category_list})