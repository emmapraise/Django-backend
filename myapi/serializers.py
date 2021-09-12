import requests
from myapi.models import *
from rest_framework import serializers

import random
from myapi.models import User

class ReadWriteSerializerMixin(object):
    """
    Overrides get_serializer_class to choose the read serializer
    for GET requests and the write serializer for POST requests.

    Set read_serializer_class and write_serializer_class attributes on a
    viewset.
    """

    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return self.get_write_serializer_class()
        return self.get_read_serializer_class()

    def get_read_serializer_class(self):
        assert self.read_serializer_class is not None, (
                "'%s' should either include a `read_serializer_class` "
                "attribute, or override the `get_read_serializer_class()` "
                "method. "
                % self.__class__.__name__
        )
        return self.read_serializer_class

    def get_write_serializer_class(self):
        assert self.write_serializer_class is not None, (
                "'%s' should either include a `write_serializer_class` "
                "attribute, or override the `get_write_serializer_class()` "
                "method. "
                % self.__class__.__name__
        )
        return self.write_serializer_class

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True)

    class Meta:
        model = User
        exclude = ['is_active', 'is_staff', 'is_superuser', 'user_code',
                   'date_joined', 'last_login', 'groups', 'user_permissions',]

    def create(self, validated_data):
        # Generates user_code and creates new User object.
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        phone = validated_data['phone']
        suffix = random.randint(10, 999)
        user_code = f'{first_name[:3].upper()}{last_name[:3].upper()}{suffix}'
        avatar = validated_data['avatar']
        user = User.objects.create_user(
            first_name=first_name,
            phone=phone,
            last_name=last_name,
            email=validated_data['email'],
            username=f'{first_name}{last_name}{suffix}',
            avatar= avatar,
            user_code=user_code,
            password=validated_data['password'],
            referral = validated_data['referral'],
        )
            
        return user

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    old_password = serializers.CharField(style={'input_type': 'password'},
                                         write_only=True, required=True)
    new_password = serializers.CharField(style={'input_type': 'password'},
                                         write_only=True, required=True)

    class Meta:
        model = User

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password reset endpoint.
    """

    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True, required=True)

    class Meta:
        model = User

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass




class CategorySerializer(serializers.ModelSerializer):
    """A serializers for all actions on Category"""
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    """A serializer for all actions on product"""
    # category = CategorySerializer()
    class Meta:
        model = Product
        fields = '__all__'

class DiscountVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountVoucher
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class ReadSaleSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only = True)
    product = ProductSerializer(read_only = True)
    # product = ProductSerializer()
    # discount_voucher = DiscountVoucherSerializer(read_only = True)

    class Meta:
        model = Sale
        fields = '__all__'

class WriteSaleSerializer(serializers.ModelSerializer):
    """A Serializer for actions on Sales."""
    # product = ProductSerializer(write_only = True)
    class Meta:
        model = Sale
        exclude = ['client', 'type']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ['status', 'reference', 'payment_mode', 'client', 'install_sale', 'type']

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        exclude = ['client']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ['client']
        
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved
        exclude = ['client']

class MessagesSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Messages sent to the client from the Admin
    """
    class Meta:
        model = Messages
        fields = '__all__'

class WriteInstallSalesSerializer(serializers.ModelSerializer):
    
    sale = WriteSaleSerializer()

    class Meta:
        model = Installmental_sales
        exclude = ['next_charge', 'amount_paid', 'status', 'authorization']

    def create(self, validated_data,):
        request = self.context.get('request', None)
        current_user = request.user.id
        quantity = validated_data['sale']['quantity']
        client = current_user
        product = validated_data['sale']['product']
        price = validated_data['sale']['price']
        status = validated_data['sale']['status']
        # print(requests.request)

        sale = Sale.objects.create(
            client_id = client,
            product = product,
            price = price,
            status = status,
            quantity = quantity,
        )
        sale.type = sales.INSTALLMENTAL
        sale.save()

        print(sale.id)

        # validated_data['sale'].pop('client')
        validated_data.pop('sale')
        print(validated_data)
        instalment = Installmental_sales.objects.create(sale_id = sale.id, **validated_data)
        return instalment

class ReadInstallSalesSerializer(serializers.ModelSerializer):
    sale = ReadSaleSerializer()
    class Meta:
        model = Installmental_sales
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    """ A serializer for action on Bank Account """

    class Meta:
        model = Bank
        fields = ['bank_name']

class BankAccountSerializer(serializers.ModelSerializer):
    """ A serializer for action on Bank Account """
    # bank = BankSerializer()
    class Meta:
        model = BankAccount
        exclude = ['client']

class WithdrawalSerializer(serializers.ModelSerializer):

    """A serializer for action on Withdrawal """

    class Meta:
        model = Withdrawal
        exclude = ['client', 'status']

class CommissionSerializer(serializers.ModelSerializer):
    """
    A Serializer for all actions on commissions 
    """
    class Meta:
        model = Commission
        fields = '__all__'
