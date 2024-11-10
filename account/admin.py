# Django Built-in modules
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.exceptions import ValidationError



# Local apps
from .forms import UserCreationForm, UserChangeForm
from gateways.models.banks import Bank
from translator.admin import TranslatorAdmin
from .models import MobilePhoneVerify, User, UserAddress
from utils.admin import DateTimeAdminMixin



# Third party import
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
    



class UserAddressInlineAdmin(admin.TabularInline):
    model = UserAddress
    extra = 0
    
    
class TransactionAdmin(admin.TabularInline):
    model = Bank
    extra = 0
    fields = (
        'id',
            'user',
            'amount',
            'tracking_code',
            'status',
    )
    readonly_fields = (
        'id',
            'user',
            'amount',
            'tracking_code',
            'status',
            'content_object',
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (
            _('اطلاعات'),
            {'fields': ('username', 'full_name', 'mobile_number', 'email', 'avatar', 'password',)}
        ),
        (
            _('لاگ'),
            {'fields': ('last_login',)}
        ),
        (
            _('مجوز ها'),
            {
                # 'classes': ('collapse',),
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
            }
        ),
        *DateTimeAdminMixin.fieldsets,
    )
    add_fieldsets = (
        (
            _('اطلاعات'),
            {
                'fields': (
                    'username', 'password1', 'password2', 'full_name', 'mobile_number', 'email', 'avatar',
                )
            }
        ),
        (
            _('مجوز ها'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
                # 'classes': ('collapse',),
            }
        ),
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('username', 'display_fullname', 'email', 'mobile_number', 'is_superuser',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    search_fields = ('username', 'full_name', 'mobile_number', 'email',)
    ordering = ('-created',)
    inlines = (UserAddressInlineAdmin, )
    

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'user_permissions':
            kwargs['queryset'] = Permission.objects.select_related('content_type')
        return super(UserAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    
        

    @admin.display(description=_('نام و نام خانوادگی'), empty_value='-')
    def display_fullname(self, obj):
        return f'{obj.full_name}'



@admin.register(MobilePhoneVerify)
class MobilePhoneVerifyAdmin(admin.ModelAdmin):
    list_display = ('mobile_number', *DateTimeAdminMixin.list_display)
