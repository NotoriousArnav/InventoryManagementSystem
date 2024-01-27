from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category_list'),
    # ... other category URLs ...
    path('products/', ProductList.as_view(), name='product_list'),
    # ... other product URLs ...
    path('product_attachments/', ProductAttachmentList.as_view(), name='attachment_list'),
    path('products/<slug:slug>/', product_detail, name='product_detail'),
]
