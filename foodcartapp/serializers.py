from .models import Order, OrderItem
from rest_framework.serializers import ModelSerializer


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'product',
            'quantity',
        ]

    
class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(
        many=True,
        allow_empty=False,
        write_only=True,
    )

    class Meta:
        model = Order
        fields = [
            'products',
            'firstname',
            'lastname',
            'phonenumber',
            'address',
        ]
    
    def create(self, validated_data):
        order = Order.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phonenumber=validated_data['phonenumber'],
            address=validated_data['address']
        )
        order_products = validated_data['products']    
        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                product=order_product.get('product'),
                quantity=order_product.get('quantity'),
                price=order_product.get('product').price,
            ) 
            for order_product in order_products]
        )
        return order
