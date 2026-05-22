from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BusSlot, Booking

admin.site.register(User, UserAdmin)
admin.site.register(BusSlot)
admin.site.register(Booking)
