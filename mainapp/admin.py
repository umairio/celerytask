from django.contrib import admin

from .models import Profile, User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "last_login",
    ]


def last_login(self, obj):
    return obj.last_login


admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "subscription_start_date", "subscription_end_date"]


admin.site.register(Profile, ProfileAdmin)
