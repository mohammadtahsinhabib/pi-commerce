from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from product.models import Category, Product, ProductReview
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "stock", "price", "category", "tax"]

    tax = serializers.SerializerMethodField(method_name="calculate_tax")
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name="category-detail",
        lookup_field="id",
    )

    def calculate_tax(self, product):
        tax_rate = Decimal("0.15")
        return product.price * tax_rate

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "product_count"]

    product_count = serializers.IntegerField(read_only=True)


class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name="get_user")
    class Meta:
        model = ProductReview
        fields = ["id", "user", "rating", "comment", "created_at","updated_at", "product"]
        read_only_fields = ["id","created_at", "updated_at", "product","user"]

    product = serializers.HyperlinkedRelatedField(
        view_name="product-detail",
        read_only=True,
        lookup_field="pk",
    )

    def get_user(self,obj):
        return SimpleUserSerializer(obj.user).data
    
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return ProductReview.objects.create(product_id=product_id, **validated_data)

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class SimpleUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name="get_user_name")
    class Meta:
        model = User
        fields = ["id", "user"]
    
    def get_user_name(self,obj):
        return obj.username or obj.get_full_name() or "Anonymous"