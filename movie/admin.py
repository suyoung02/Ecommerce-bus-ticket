from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Seat)
admin.site.register(Trip)
admin.site.register(Payment)