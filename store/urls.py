from django.urls import path
from store import views
from . import views


urlpatterns = [
    # leave as empty string for base url
    path('',views.store, name="Store"), # this is the home page
    path('cart/',views.cart, name="Cart"),
    path('checkout/',views.checkout, name="Checkout"),
    path('healthtips/',views.healthtips, name="healthtips"),
    path('#items/', views.items_view, name='items'),

    #try changing the name if everything works fine after running server
    path('update_item/',views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name="process_order"),
    
    path('fetch-products/<str:category_id>/', views.fetch_products, name='fetch_products'),
    path('fetch-category/', views.fetch_category, name='fetch_category'),


]

# main html e url e always name gula ekhane jerkom ase oita dite hobe