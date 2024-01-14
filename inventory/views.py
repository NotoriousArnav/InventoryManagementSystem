from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, ProductAttachment
from .serializer import CategorySerializer, ProductSerializer, ProductAttachmentSerializer
from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.

class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    # ... other views for categories (retrieve, create, update, delete) ...

class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # ... other views for products (retrieve, create, update, delete) ...

class ProductAttachmentList(APIView):
    def get(self, request):
        attachments = ProductAttachment.objects.all()
        serializer = ProductAttachmentSerializer(attachments, many=True)
        return Response(serializer.data)

    # ... other views for attachments (retrieve, create, update, delete) ...