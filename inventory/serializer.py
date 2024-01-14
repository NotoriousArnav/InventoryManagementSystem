from rest_framework import serializers
from .models import Category, Product, ProductAttachment

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'product_count')

class ProductSerializer(serializers.ModelSerializer):
    total_count = serializers.IntegerField(read_only=True)
    category = CategorySerializer(many=True)
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category', 'price', 'qty', 'total_count', 'attachments')

    def get_attachments(self, obj):
        return ProductAttachmentSerializer(obj.productattachment_set.all(), many=True).data

class ProductAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttachment
        fields = ('id', 'file', 'file_name')