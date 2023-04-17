from rest_framework import serializers
from .models import CustomUser, Product, Cart, Order


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['fio', 'email', 'password']

    def save(self, **kwargs):
        user = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['fio'],
            fio=self.validated_data['fio'],
            password=self.validated_data['password']
        )
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['products']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
