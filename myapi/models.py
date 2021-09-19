from mysite.enums import payments, sales, wallets
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from mysite.enums.payments import payment_types, payment_status, withdrawal_status
from mysite.enums.sales import sale_status, installment_status, sale_types
from mysite.enums.wallets import wallet_status, wallet_types

# Create your models here.
class UserManager(BaseUserManager):
    """Define a model manager for User model with email login."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """This represents a User object within our system"""

    first_name = models.CharField( max_length=25, blank=True)
    last_name = models.CharField( max_length=25, blank=True,)
    phone = models.CharField( max_length=25, blank=True)                                 
    email = models.EmailField(unique=True)
    user_code = models.CharField(max_length=50, blank=True, null=True, unique=True)
    avatar = models.ImageField(null = True, blank = True)
    username = models.CharField(max_length=50, null=True, blank=True, unique=True)
    residential_address = models.TextField(blank=True, null = True)
    referral = models.ForeignKey(to='User', null=True, blank=True, on_delete=models.SET_NULL, related_name='downline', default=1)
    country = models.CharField(max_length=20, blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

class AuthCard(models.Model):
    client = models.ForeignKey(to='User', on_delete=models.CASCADE)
    authorization_code = models.CharField(max_length=30)
    card_type = models.CharField(max_length=30)
    last4 = models.IntegerField()
    exp_month = models.CharField(max_length=2)
    exp_year = models.CharField(max_length=4)
    bin = models.CharField(max_length=30)
    bank = models.CharField(max_length=30)
    channel = models.CharField(max_length=30)
    signature = models.CharField(max_length=30, unique=True)
    is_reusable = models.BooleanField(default=False)
    country_code = models.CharField(max_length=30)
    account_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.account_name

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    initial_price = models.DecimalField(decimal_places=2, max_digits=10, blank = True, null = True)
    installment_price = models.DecimalField(decimal_places=2, max_digits=10, blank = True, null = True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, blank=True, null=True)
    banner = models.ImageField()
    description = models.TextField()
    specifications = models.TextField(blank=True, null = True)
    top_deal = models.BooleanField(default=False)
    deal_of_today = models.BooleanField(default=False)
    hot_deal = models.BooleanField(default=False)
    quanity = models.IntegerField(default = 50)
    pictures = models.URLField()
    createat = models.DateTimeField(auto_now_add=True)
    updateat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Plan(models.Model):
    product = models.ForeignKey(to='Product', on_delete = models.CASCADE, blank=True, null=True)
    limit = models.IntegerField(default=3)
    interval_amount = models.DecimalField(decimal_places=2, max_digits=10,)

    def __str__(self):
        return f'({self.product}) of interval ({self.interval_amount})'

class Shipping(models.Model):
    client = models.ForeignKey(to = 'User', on_delete= models.CASCADE)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length= 20)
    sate = models.CharField(max_length=20)
    street_address = models.TextField()
    email = models.EmailField()
    additional_info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.client} shipped to {self.name}'

class Cart(models.Model):
    client = models.ForeignKey(to= 'User', on_delete=models.CASCADE)
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.client} cart {self.product}'

class Saved(models.Model):
    client = models.ForeignKey(to= 'User', on_delete=models.CASCADE)
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.client} saved {self.product}'

class Payment(models.Model):
    client = models.ForeignKey(to='User', on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    amount = models.FloatField()
    payment_mode = models.CharField(max_length=18, blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    evidence = models.ImageField(blank=True, null=True)
    status = models.IntegerField(choices=payment_status(), default=payments.PENDING)
    type = models.CharField(blank=True, null=True, max_length=30, choices=payment_types())
    install_sale = models.ForeignKey(to='Installmental_sales', on_delete=models.CASCADE, blank=True, null=True)
    payment_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updateat = models.DateTimeField(auto_now=True, blank= True, null=True)

    def __str__(self):
        return f'[{self.payment_date}] {self.status} - {self.client} paid' \
               f' {self.amount}'

class Sale(models.Model):
    client = models.ForeignKey(to='User', on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    discount_voucher = models.ForeignKey(to='DiscountVoucher',on_delete=models.PROTECT, null=True,
                                         blank=True)
    status = models.IntegerField(choices=sale_status(), default=sales.PENDING)
    type = models.CharField(blank=True, null=True, max_length=30, choices=sale_types(), default=sales.OUTRIGHT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.client}) {self.product}'

class Installmental_sales(models.Model):
    sale = models.OneToOneField(to='Sale', on_delete=models.CASCADE)
    amount_paid = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    is_commission_approved = models.BooleanField(default=False)
    install_limit = models.IntegerField(default=0)
    last_charge = models.DateField(auto_now=True)
    next_charge = models.DateField(blank=True, null=True)
    status = models.IntegerField(choices=installment_status(), default=sales.PENDING)
    authorization = models.ForeignKey(to='AuthCard', on_delete=models.DO_NOTHING, blank=True, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.sale}) amount paid ({self.amount_paid}) next payment date {self.next_charge}'

class Messages(models.Model):
    client = models.ForeignKey(to='User', on_delete=models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class DiscountVoucher(models.Model):
    code = models.CharField(max_length=10)
    amount = models.FloatField()
    is_used = models.BooleanField(default=False)
    # created_by = models.ForeignKey(to='Admin', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.code} ({self.amount})'

class Withdrawal(models.Model):
    recipient_code = models.CharField(max_length=100, blank=True)
    amount = models.IntegerField()
    account = models.ForeignKey(to='BankAccount', on_delete=models.DO_NOTHING, null=True)
    description = models.TextField(null=True)
    client = models.ForeignKey(to='User', on_delete=models.DO_NOTHING)
    status = models.SmallIntegerField(default=payments.PENDING,
                                      choices=withdrawal_status())
    reference = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.account_number} ({self.amount})'

class Bank(models.Model):
    bank_name = models.CharField(max_length=50, unique=True)
    bank_code = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.bank_name

class BankAccount(models.Model):
    client = models.ForeignKey(to='User', on_delete=models.DO_NOTHING)
    bank = models.ForeignKey(to='Bank', on_delete=models.PROTECT)
    account_number = models.CharField(max_length=20, unique=True)
    account_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.account_number}'

class Commission(models.Model):
    client = models.ForeignKey(to='User', on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    percentage = models.FloatField(default=4)
    detail = models.CharField(max_length=250, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.client} get {self.amount}'

class Wallet(models.Model):
    client = models.ForeignKey(to='User', on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} has {self.balance} balance'

class WalletTranscation(models.Model):
    wallet = models.ForeignKey(to='Wallet', on_delete=models.CASCADE)
    amount = models.FloatField()
    type = models.CharField(blank=True, null=True, max_length=30, choices=wallet_types())
    status = models.IntegerField(choices=wallet_status(), default=wallets.PENDING)

    def __str__(self):
        return self.amount
