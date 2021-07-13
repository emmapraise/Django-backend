from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from myapi.models import *
# Register your models here.
admin.site.register(User, UserAdmin,)
admin.site.register([ Category, Product, Cart, Shipping, Saved, Payment, Sales])