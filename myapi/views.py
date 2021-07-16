import json
from myapi.serializers import *
from myapi.models import *
from myapi.serializers import UserSerializer
from myapi.models import User
from django.db import IntegrityError
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from paystackapi.customer import Customer
from paystackapi.misc import Misc
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
from paystackapi.transfer import Transfer
from paystackapi.trecipient import TransferRecipient

from mysite.enums import payments
from django.conf import settings
# Create your views here.
paystack_secret_key = settings.PAYSTACK_SECRET_KEY
paystack = Paystack(secret_key=paystack_secret_key)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all users to be viewed or edited.

    Available  Endpoint
    register: https://ideathinker-django.herokuapp.com/register
    Login: https://ideathinker-django.herokuapp.com/login
    Logout: https://ideathinker-django.herokuapp.com/logout
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        # try:
        response = super().create(request, args, **kwargs)
        user = User.objects.get(email=response.data['email'])
        response = {
            'data': response.data,
            'message': 'User created successfully.',
            'status': 'success'
        }
        # except IntegrityError:
            # response = {
            #     'data': {},
            #     'message': 'Existing account found with this email.',
            #     'status': 'failure'
            # }
        return Response(data=response, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint for category"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []

class ProductViewSet(viewsets.ModelViewSet):
    """API endpoint for category"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []



class SaleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows purchases to be viewed or edited.
    """
    queryset = Sales.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            amount =  json.dumps(
                float(serializer.validated_data['price']) * 100)
            email = request.user.email

            sale = Sales.objects.create(
                client_id = request.user.id,
                product = serializer.validated_data['product'],
                price = serializer.validated_data['price'],
            )
            
            sale.save()

            response = Transaction.initialize(amount=amount, email=email)

            payment = Payment.objects.create(
                client_id = request.user.id,
                type = payments.OUTRIGHT,
                amount=serializer.validated_data['price'],
                reference=response['data']['reference'],
            )
            payment.save()
            return redirect(response['data']['authorization_url'])
    
# class Installmental_SaleViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint for all installmental sales 
#     """
#     queryset = Installmental_sales
#     serializer_class = Installmental_salesSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             amount =  json.dumps(
#                 float(serializer.validated_data['price']) * 100)
#             email = request.user.email

#             sale = Sales.objects.create(
#                 client_id = request.user.id,
#                 product = serializer.validated_data['product'],
#                 price = serializer.validated_data['price'],
#             )
            
#             sale.save()

#             response = Transaction.initialize(amount=amount, email=email)

#             payment = Payment.objects.create(
#                 client_id = request.user.id,
#                 sale_id = sale.id,
#                 amount=serializer.validated_data['price'],
#                 reference=response['data']['reference'],
#             )
#             payment.save()

            
#             return redirect(response['data']['authorization_url'])


class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all actions on Cart
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

class ShippingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all actions on shipping
    """
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [permissions.IsAuthenticated]

class SavedViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all actions on saved product
    """
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentViewSet(viewsets.ModelViewSet):
    """ API endpoint for actions on payment """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail = False, methods = ['POST'])
    def topup(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            amount =  json.dumps(
                float(serializer.validated_data['amount']) * 100)
            email = request.user.email

            response = Transaction.initialize(amount=amount, email=email)

            payment = Payment.objects.create(
                client_id = request.user.id,
                type = payments.TOUPUP,
                amount =serializer.validated_data['amount'],
                reference=response['data']['reference'],
            )
            payment.save()

            
            return redirect(response['data']['authorization_url'])

    # @action(detail=False, methods=['post'])
    # def receive_event(self, request):
    #     """ Webook to recieve payment event """
    #     response_data = ''
    #     data = request.data
    #     if data['event'] == 'charge.success':
    #         response_data = transaction_success(data['data'])
    #     elif data['event'] == 'transfer.failed':
    #         response_data = transfer_failed(data['data'])
    #     elif data['event'] == 'transfer.success':
    #         response_data = transfer_success(data['data'])
    #     return Response(status=status.HTTP_200_OK, data=response_data)

    @action(detail=False, methods=['GET'])
    def verify_payment(self, request):
        """GET method to verify payment """
        ref = request.GET['reference']
        response = Transaction.verify(reference=ref)
        if response['data']['status'] == 'success':
            pay = Payment.objects.get(
                reference=response['data']['reference'])
            pay.status= payments.APPROVED
            pay.save()

            if pay.type == payments.TOUPUP:
                user = User.objects.get(id = request.user.id)
                user.wallet_balance = user.wallet_balance + (response['data']['amount'] / 100)
                user.save()
            authcard = AuthCard.objects.create(
                client_id = request.user.id,
                authorization_code = response['data']['authorization']['authorization_code'],
                card_type = response['data']['authorization']['card_type'],
                last4 = response['data']['authorization']['last4'],
                exp_month = response['data']['authorization']['exp_month'],
                exp_year = response['data']['authorization']['exp_year'],
                bin = response['data']['authorization']['bin'],
                bank = response['data']['authorization']['bank'],
                channel = response['data']['authorization']['channel'],
                signature = response['data']['authorization']['signature'],
                is_reusable = response['data']['authorization']['reusable'],
                country_code = response['data']['authorization']['country_code'],
                account_name = response['data']['authorization']['account_name'], 
            )
            authcard.save()
        return Response(response, status=status.HTTP_200_OK)