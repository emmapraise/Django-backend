import json
from datetime import date, timedelta
from myapi.serializers import *
from myapi.models import *
from myapi.serializers import UserSerializer
from myapi.models import User

from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView, get_object_or_404

from paystackapi.customer import Customer
from paystackapi.misc import Misc
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
from paystackapi.transfer import Transfer
from paystackapi.trecipient import TransferRecipient

from mysite.helpers.paystack import resolve_account
from mysite.helpers.email import *
from mysite.enums import payments
from django.conf import settings
# Create your views here.
paystack_secret_key = settings.PAYSTACK_SECRET_KEY
paystack = Paystack(secret_key=paystack_secret_key)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all users to be viewed or edited.

    Available  Endpoint
    register: https://etsea.herokuapp.com/api/register/
    Login: https://etsea.herokuapp.com/api/login
    Logout: https://etsea.herokuapp.com/api/logout
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, args, **kwargs)
            user = User.objects.get(email=response.data['email'])
            Wallet.objects.create(client_id = user.id)
            response = {
                'data': response.data,
                'message': 'User created successfully.',
                'status': 'success'
            }
            if send_welcome(user, request.META.get('HTTP_REFERER')):
                response['message'] += 'Welcome email sent successfully.'

        except IntegrityError:
            response = {
                'data': {},
                'message': 'Existing account found with this email.',
                'status': 'failure'
            } 
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

class ActivateAPIView(APIView):
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_token.check_token(user, token):
            # activate user:
            user.is_active = True
            user.save()

            return Response(status=status.HTTP_200_OK, data={
                'message': 'Email verification successful.'
            })

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                'message': 'Activation link is invalid!'
            })


class ChangePasswordAPIView(UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        """
        GET method on password

        Args:
            self (obj)
            queryset (obj)

        Returns:
            obj (dic): the current user
        """
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        """
        PUT method to change user password

        Args:
            self (obj)
            request (obj)

        Returns:
            Response (dic): status code
        """
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(
                    serializer.data.get("old_password")):
                data = {
                    'errors': {
                        "old_password": ["Wrong password."]
                    }
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            changed_password(self.object.email)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendResetPasswordAPIView(APIView):
    """
    An endpoint for sending email to reset forgotten password.
    """
    permission_classes = []

    def post(self, request):
        try:
            print(f'post data: {request.data}')
            user = User.objects.get(email=request.data['email'])
            print(f'user object: {UserSerializer(user).data}')

            # send password reset email
            password_reset(user, request.META.get('HTTP_REFERER'))
            status_code = status.HTTP_200_OK
            response = {
                'data': {},
                'message': 'Password reset email sent.',
                'status': 'success'
            }
        except User.DoesNotExist:
            response = {
                'data': {},
                'message': 'User with that email address not found.',
                'status': 'failure'
            }
            status_code = status.HTTP_404_NOT_FOUND
        return Response(status=status_code, data=response)


class ResetPasswordAPIView(APIView):
    """
    An endpoint for resetting forgotten password.
    """
    permission_classes = []

    def get(self, request, uidb64, token):
        response = {
            'data': {},
            'message': 'Invalid reset password link!',
            'status': 'failure'
        }
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_token.check_token(user, token):
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_token.make_token(user)
            reset_link = f'{get_current_site(request)}/api/reset-password/{uid}/{token}/'
            response = {
                'data': {
                    'reset_link': reset_link
                },
                'message': 'Link verified. Post new password to new link.',
                'status': 'success'
            }
            status_code = status.HTTP_200_OK
        return Response(status=status_code, data=response)

    def post(self, request, uidb64, token):
        response = {
            'data': {},
            'message': 'Invalid reset password link!',
            'status': 'failure'
        }
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_token.check_token(user, token):
            user.set_password(request.data['new_password'])
            user.save()

            # send changed password email to user
            changed_password(user.email)
            response = {
                'data': {},
                'message': 'Password successfully reset.',
                'status': 'success'
            }
            status_code = status.HTTP_200_OK
        return Response(status=status_code, data=response)



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
    
class WalletViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all actions on Wallet
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
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
                wallet = Wallet.objects.get(client_id = request.user.id)
                wallet.balance = wallet.balance + (response['data']['amount'] / 100)
                wallet.save()
                WalletTranscation.objects.create(
                    wallet_id = wallet.id,
                    amount = (response['data']['amount'] / 100),
                    type = wallets.TOPUP,
                    status = wallets.PAID
                )
                
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
                try:
                    authcard = AuthCard.objects.get(signature = response['data']['authorization']['signature'])
                except AuthCard.DoesNotExist:
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
                        is_reusable = response['data']['authorization']['reusable'],
                        country_code = response['data']['authorization']['country_code'],
                        account_name = response['data']['authorization']['account_name'], 
                        defaults = {'signature': response['data']['authorization']['signature']}
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

    @action(detail = True, methods=['POST'])
    def approve(self, request, pk=None):
        commission = self.get_object()
        # serializer = CommissionSerializer(data = request.data)
        commission.is_approved = True

class ReferralAPIView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        code = str(kwargs.get('ref'))
        print(code)

        try:
            user = User.objects.get(user_code = code)
            id = user.id
            first_name = user.first_name
            last_name = user.last_name
            return Response(data= {'referral_id': id, 'referral_first_name': first_name, 'referral_last_name': last_name})
        except :
            
            return Response(data= {'message': 'No user found'})

class PendingCommissionAPIView(APIView):
    """
    API View of actions on Pending Commission
    """

    def get(self, request):
        """
        GET method for pending commission

        Args:
            self (obj)
            request (obj)

        Returns:
            Response (dic): status, data and message
        """
        commission = Commission.objects.all()
        if commission.exists():
            commission = commission.values('id', 'amount', 'client__first_name', 'client__last_name')

        return Response(data={
            'commission': commission
        })

    def post(self, request):
        """
        POST method on pending commission

        Args:
            self (obj)
            request (obj)

        Returns:
            Response (dic): status, data and message
        """
        request_id = request.data.get('commission_id', 0)
        is_approved = bool(request.data.get('is_approved', False))
        commission_request = Commission.objects.filter(id=request_id)
        if commission_request.exists():
            if is_approved is True:
                commission_request.update(status=requests.APPROVED)
            elif is_approved is False:
                commission_request.update(status=requests.DISAPPROVED)
        return Response(data={
            'commission_request': commission_request
        })

