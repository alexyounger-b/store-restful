from django.contrib import admin

from apps.authentication.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ("email", "first_name", "last_name")
