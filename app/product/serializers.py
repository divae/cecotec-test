from rest_framework import serializers

from core.models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product object"""

    class Meta:
        model = Product
        fields = ('id', 'name', 'price')
        read_only_Fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )

    class Meta:
        model = Order
        fields = ('id', 'name', 'number', 'products')
        read_only_Fields = ('id',)
