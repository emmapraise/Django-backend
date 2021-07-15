from myapi.models import *
from rest_framework import serializers

from myapi.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True)

    class Meta:
        model = User
        exclude = ['is_active', 'is_staff', 'is_superuser',
                   'date_joined', 'last_login', 'groups', 'user_permissions']

    def create(self, validated_data):
        # Generates user_code and creates new User object.
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        phone = validated_data['phone']
        avatar = validated_data['avatar']
        user = User.objects.create_user(
            first_name=first_name,
            phone=phone,
            last_name=last_name,
            email=validated_data['email'],
            username=validated_data['email'],
            avatar= avatar,
            password=validated_data['password'],
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    """A serializers for all actions on Category"""
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    """A serializer for all actions on product"""
    class Meta:
        model = Product
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved
        fields = '__all__'

# class Installmental_salesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Installmental_sales
#         fields = '__all__'