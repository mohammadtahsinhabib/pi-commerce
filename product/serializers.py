from decimal import Decimal
from rest_framework import serializers
from product.models import Category, Product,ProductReview


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name","description","stock", "price", "category","tax"]


    tax = serializers.SerializerMethodField(method_name="calculate_tax")
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name="category-detail",
        lookup_field="id",)
    
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
        fields = ["id", "name", "description","product_count"]
    
    product_count = serializers.IntegerField(read_only=True)


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ["id", "product", "rating", "comment", "created_at"]
    
    product = serializers.HyperlinkedRelatedField(
        queryset=Product.objects.all(),
        view_name="products-detail",
        lookup_field="id",
    )
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value