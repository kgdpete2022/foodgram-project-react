from django.contrib import admin
from users.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "subscriber",
    )
    list_filter = (
        "author",
        "subscriber",
    )
