from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render, HttpResponse
from .serializer import CategorySerializer, ProductSerializer, ProductAttachmentSerializer
from .models import *

# Create your views here.

@api_view(['GET'])
def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

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
