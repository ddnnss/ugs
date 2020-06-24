from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import *


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ( 'phone','first_name','last_name','balance')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone'),
        }),
    )
    list_display = ('id','email', 'first_name','last_name',  'phone')

    ordering = ('id',)
    search_fields = ('email', 'id', 'phone','first_name','last_name',)


admin.site.register(BalanceFreeze)
admin.site.register(Bet)
admin.site.register(Log)
admin.site.register(Payment)
admin.site.register(Withdraw)
