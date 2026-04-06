from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Interest

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_flagged', 'flag_reason', 'date_joined')
    list_filter = ('is_flagged', 'is_superuser')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('bio', 'profile_pic', 'interests', 'is_flagged', 'flag_reason')}),
    )

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)