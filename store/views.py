from django.shortcuts import render

# Create your views here.

def store(request):
    context = {}
    return render(request,'store/store.html',context)


def cart(request):
    context = {}
    return render(request,'store/cart.html',context)


def checkout(request):
    context = {}
    return render(request,'store/checkout.html',context)

def index(request):
    diction = {}
    return render(request, 'store/index.html', context=diction)

