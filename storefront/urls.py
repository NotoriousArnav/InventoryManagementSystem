from django.urls import path
from .views import register, login_view, custom_logout

app_name = 'storefront'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
    # Add other URLs for your storefront
]
