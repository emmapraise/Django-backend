import json
from datetime import date, timedelta
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

from mysite.helpers.paystack import resolve_account
from mysite.enums import payments
from django.conf import settings
# Create your views here.
paystack_secret_key = settings.PAYSTACK_SECRET_KEY
paystack = Paystack(secret_key=paystack_secret_key)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all users to be viewed or edited.

    Available  Endpoint
    register: https://etsea.herokuapp.com/register/
    Login: https://etsea.herokuapp.com/login
    Logout: https://etsea.herokuapp.com/logout
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

class SaleViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows purchases to be viewed or edited.
    """
    queryset = Sale.objects.all()
    read_serializer_class = ReadSaleSerializer
    write_serializer_class = WriteSaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, args, **kwargs)
        amount =  json.dumps(float(response.data['price']) * 100)
        email = request.user.email

        resp = Transaction.initialize(amount=amount, email=email)

        payment = Payment.objects.create(
            client_id = request.user.id,
            type = payments.OUTRIGHT,
            amount=response.data['price'],
            reference=resp['data']['reference'],
        )
        payment.save()
        return redirect(resp['data']['authorization_url'])
    
class Installmental_SaleViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    """
    API endpoint for all installmental sales 
    """
    queryset = Installmental_sales.objects.all()
    read_serializer_class = ReadInstallSalesSerializer
    write_serializer_class = WriteInstallSalesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        amount =  json.dumps(float(response.data['amount']) * 100)
        email = request.user.email

        resp = Transaction.initialize(amount=amount, email=email)

        payment = Payment.objects.create(
            client_id = request.user.id,
            type = payments.INSTALLMENT,
            install_sale_id =response.data['id'],
            amount=response.data['amount'],
            reference=resp['data']['reference'],
        )
        payment.save()
        return redirect(resp['data']['authorization_url'])

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

class MessagesViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all actions on saved product
    """
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
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

            user = User.objects.get(id = request.user.id)
            if pay.type == payments.TOUPUP:
                
                user.wallet_balance = user.wallet_balance + (response['data']['amount'] / 100)
                

            elif pay.type == payments.INSTALLMENT:

                in_sale = Installmental_sales.objects.get(id = pay.install_sale.id)
                in_sale.install_limit = in_sale.install_limit -1
                if in_sale.install_limit <= 0:
                    in_sale.status = sales.COMPLETED
                    in_sale.amount_paid = in_sale.amount_paid + in_sale.amount
                    in_sale.next_charge = None
                    
                else:
                    in_sale.status = sales.PAYING
                    in_sale.next_charge = (date.today() + timedelta(days= 30))
                    in_sale.amount_paid = in_sale.amount_paid + in_sale.amount
                    
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
                in_sale.authorization = authcard
                in_sale.save()

                if user.referral != None:
                    commission = Commission.objects.create(
                        client = user.referral,
                        amount = in_sale.amount * 0.25,
                    )
                    commission.save()
            user.save()
        return Response(response, status=status.HTTP_200_OK)

class BankAccountViewSet(viewsets.ModelViewSet):
    """
        Viewset for adding Bank account
    """
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            bank_name = serializer.validated_data['bank']
            account_number = serializer.validated_data['account_number']
            bank_code = Bank.objects.get(bank_name = bank_name).bank_code
            
            response = resolve_account(paystack_secret_key, account_number, bank_code)
            account = BankAccount.objects.create(
                client_id = request.user.id,
                bank = bank_name,
                account_number = account_number,
                account_name = response['data']['account_name']
            )
            account.save()
            return Response(response['data'])

class BankViewSet(viewsets.ModelViewSet):
    """API endpoint for action on Bank """
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [permissions.IsAuthenticated]

class ListOfBankAPIView(APIView):
    """
        Get the list of Banks and the Bank Code
    """

    def get(self, request):
        """GET Method for list of Banks """
        response = Misc.list_banks()
        for i in range(0, len(response['data'])):
            bank = Bank.objects.create(
                bank_name=response['data'][i]['name'],
                bank_code=response['data'][i]['code'])
            bank.save()
        return Response(data=response, status=status.HTTP_200_OK)

class WithdrawalViewSet(viewsets.ModelViewSet):
    """API View for actions on Withdrawal """
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        """POST method for Withdrawal """
        serializer = WithdrawalSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(id = request.user.id)
            if user.wallet_balance >= serializer.validated_data['amount']:

                amount = json.dumps(
                    int(serializer.validated_data['amount']) * 100)
                account = serializer.validated_data['account']
                reason = serializer.validated_data['description']
                account_details = BankAccount.objects.get(account_number = account)
                bank_code = Bank.objects.get(bank_name=account_details.bank).bank_code
                

                # # Verify and Create Transfer for Customers
                trans_rep = TransferRecipient.create(
                    type="nuban",
                    name=account_details.account_name,
                    description= reason,
                    account_number=account_details.account_number,
                    bank_code=bank_code)

                if trans_rep['status']:
                    response = Transfer.initiate(source="balance", 
                    reason=reason,
                    amount=amount,
                    recipient=trans_rep['data']['recipient_code'])

                    withdraw = Withdrawal.objects.create(
                        amount=serializer.validated_data['amount'],
                        description=reason,
                        recipient_code=trans_rep['data']['recipient_code'],
                        account = serializer.validated_data['account'],
                        client_id = request.user.id,
                        # reference = response['data']['reference']
                    )
                    withdraw.save()
                #     wallet = Wallet.objects.filter(
                #         client=request.user.client.id)
                #     wallet.balance = wallet.balance - serializer.validated_data[
                #         'amount']
                #     wallet.save()

            return Response(status=status.HTTP_200_OK,
                            data=response)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
        # wallet = WalletTransaction.objects.create(
        #     amount=serializer.validated_data['amount'],
        #     reference=response['data']['reference'],
        #     type=serializer.validated_data['type'],
        #     )
        # wallet.save()

class CommissionViewSet(viewsets.ModelViewSet):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = [permissions.IsAuthenticated]
