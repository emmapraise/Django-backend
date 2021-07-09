from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

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

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, blank=True, null=True)
    banner = models.ImageField()
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    on_flash_sale = models.BooleanField(default=False)
    pictures = models.URLField()
    createat = models.DateTimeField(auto_now_add=True)
    updateat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
