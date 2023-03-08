from django.contrib import admin
from .models import User, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'team')

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    readonly_fields = ('code', 'expiration', 'created_at')