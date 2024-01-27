from django.urls import path
from .views import *

app_name = 'storefront'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('', home, name="home"),
    path('p/<slug:product_slug>/', product_view, name='product_view'),
    # Add other URLs for your storefront
]
