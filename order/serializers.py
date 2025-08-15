from rest_framework import serializers

from product.models import Product

from .models import Cart, CartItem


class SimpleProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "price"]
        read_only_fields = [
            "id",
            "name",
            "price",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField(method_name="get_total")

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]
        read_only_fields = ["id", "product", "total_price"]

    def get_total(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name="get_grand_total")

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "grand_total"]
        read_only_fields = ["id"]

    def get_grand_total(self, cart: Cart):
        total = 0
        for item in cart.items.all():
            total += item.product.price * item.quantity
        return total


class AddItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]

    def save(self, **kwargs):
        cart_id = self.context.get("cart_id")
        product_id = self.validated_data.get("product_id")
        quantity = self.validated_data.get("quantity")

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value


class UpdateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value
