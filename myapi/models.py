from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from mysite.enums.payments import withdrawal_status, payment_status, \
    transaction_types
from mysite.enums.sales import sale_status, installment_status

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

    first_name = models.CharField( max_length=25,
                                  blank=True)
    last_name = models.CharField( max_length=25, blank=True,
                                 )
    phone = models.CharField( max_length=25,
                                   blank=True)                                 
    email = models.EmailField(unique=True)
    avatar = models.ImageField(null = True, blank = True)
    residential_address = models.TextField(blank=True, null = True)
    country = models.CharField(max_length=20, blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

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
    signature = models.CharField(max_length=30)
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
    promo_price = models.DecimalField(decimal_places=2, max_digits=10, blank = True, null = True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, blank=True, null=True)
    banner = models.ImageField()
    description = models.TextField()
    specifications = models.TextField(blank=True, null = True)
    top_deal = models.BooleanField(default=False)
    deal_of_today = models.BooleanField(default=False)
    hot_deal = models.BooleanField(default=False)
    quanity_left = models.IntegerField(default = 10)
    total_quanity = models.IntegerField(default = 50)
    pictures = models.URLField()
    createat = models.DateTimeField(auto_now_add=True)
    updateat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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
    status = models.IntegerField(choices=payment_status(), default=0)
    sale = models.ForeignKey(to='Sales', on_delete=models.DO_NOTHING, blank=True, null=True)
    payment_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updateat = models.DateTimeField(auto_now=True, blank= True, null=True)

    def __str__(self):
        return f'[{self.payment_date}] {self.status} - {self.client} paid' \
               f' {self.amount}'

class Sales(models.Model):
    client = models.ForeignKey(to='User', on_delete=models.PROTECT)
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    discount_voucher = models.ForeignKey(to='DiscountVoucher',on_delete=models.PROTECT, null=True,
                                         blank=True)
    # is_commission_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.client}) {self.product}'

# class Installmental_sales(models.Model):
#     # sales = models.OneToOneField(to='Sales', on_delete=models.CASCADE)
#     client = models.ForeignKey(to='User', on_delete=models.PROTECT)
#     product = models.ForeignKey(to='Product', on_delete=models.CASCADE)
#     price = models.FloatField(default=0)
#     amount_paid = models.FloatField(default=0)
#     install_months = models.IntegerField(default=0)
#     next_payment_date = models.DateField(blank=True, null=True)
#     status = models.IntegerField(choices=installment_status(), default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f'({self.sale}) amount paid ({self.amount_paid}) next payment date {self.next_payment_date}'

class DiscountVoucher(models.Model):
    code = models.CharField(max_length=10)
    amount = models.FloatField()
    is_used = models.BooleanField(default=False)
    # created_by = models.ForeignKey(to='Admin', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.code} ({self.amount})'