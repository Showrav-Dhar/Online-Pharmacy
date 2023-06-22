from django.urls import path
from store import views


urlpatterns = [
    # leave as empty string for base url
    path('',views.store, name="store"), # this is the home page
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout")
    #try changing the name if everything works fine after running server
]