from decimal import Decimal
from rest_framework import serializers
from product.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name","description","stock", "price", "category","tax"]


    tax = serializers.SerializerMethodField(method_name="calculate_tax")
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name="view-single-category",
        lookup_field="id",)
    
    def calculate_tax(self, product):
        tax_rate = Decimal("0.15")
        return product.price * tax_rate

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description","product_count"]
    
    product_count = serializers.IntegerField(read_only=True)