# django Build-in
from django.contrib import admin

# Local Apps
from .models import Member
from utils.admin import DateTimeAdminMixin


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'email',
        )}),
        *DateTimeAdminMixin.fieldsets,
    )
    readonly_fields = (*DateTimeAdminMixin.readonly_fields,)
    list_display = ('email',)
    list_per_page = 50
    search_fields = ('email',)
