from django.core.exceptions import PermissionDenied
from uuid import uuid4
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from order.models import Cart, CartItem, Order, OrderItem


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order(user_id, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id, user_id=user_id)
        except ObjectDoesNotExist:
            raise ValueError("Cart not found for this user.")

        cart_items = cart.items.select_related("product").all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(
            user=cart.user,
            total_price=total_price,
        )

        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                total_price=item.product.price * item.quantity,
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)
        cart.items.all().delete()
        return order

    @staticmethod
    def cancel_order(order , user):
        if order.user != user:
            raise ValueError("You do not have permission to cancel this order.")

        if order.is_staff:
            order.status = Order.CANCELLED
            order.save()   
            return order

        if order.user != user:
            raise PermissionDenied("You do not have permission to cancel this order.")

        order.status = Order.CANCELLED
        order.save()
        return order
