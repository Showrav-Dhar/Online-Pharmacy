from django.urls import path
from store import views


urlpatterns = [
    # leave as empty string for base url
    path('',views.store, name="Store"), # this is the home page
    path('cart/',views.cart, name="Cart"),
    path('checkout/',views.checkout, name="Checkout")
    #try changing the name if everything works fine after running server
]

# main html e url e always name gula ekhane jerkom ase oita dite hobe