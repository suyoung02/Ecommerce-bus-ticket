from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username','last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'username')   # Các trường có gắn link dẫn đến trang detail
    readonly_fields = ('last_login', 'date_joined')     # Chỉ cho phép đọc
    ordering = ('-date_joined',)     # Sắp xếp theo chiều ngược

    # Bắt buộc phải khai báo
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)