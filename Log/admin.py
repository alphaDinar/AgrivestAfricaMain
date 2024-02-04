from django.contrib import admin
from .models import User,Profile,Wallet,Balance

admin.site.register(User)

admin.site.register(Profile)

admin.site.register(Wallet)
admin.site.register(Balance)
