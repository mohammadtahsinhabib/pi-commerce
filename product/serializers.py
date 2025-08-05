from decimal import Decimal

from rest_framework import serializers

from product.models import Category, Product


class CategorySerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500)


class ProductSerializer(serializers.Serializer):
    """
    Do the job of assigining data to the fields
    product_data = {"id": product.id, "name": product.name, "price": product.price}
    """

    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    raw_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="price"
    )  # source to rename fields
    tax = serializers.SerializerMethodField(method_name="get_tax")
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name="view-single-category",
        lookup_field="id",
    )

    """
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category.id')
    category_name = serializers.CharField(source='category.name')
    category = CategorySerializer() # to show category data in the product serializer
    """

    def get_tax(self, product):
        return round(product.price * Decimal(0.1), 2)
