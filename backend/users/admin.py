from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Follow


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
    )

    search_fields = (
        "username",
        "email",
    )
    list_filter = (
        "id",
        "username",
        "email",
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "follower",
    )
    list_filter = (
        "author",
        "follower",
    )
