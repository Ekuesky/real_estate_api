from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import ContentView


# @admin.register(ContentView)
# class ContentViewAdmin(admin.ModelAdmin):
#     list_display = ["content_object", "user", "viewer_ip", "created_at"]
#
#     def has_add_permission(self, request):
#         return False  # Disable adding new content views
#     def has_change_permission(self, request, obj=None):
#         return False  # Disable editing existing content views


class ContentViewInline(GenericTabularInline):
    model = ContentView
    extra = 0
    readonly_fields = ["user", "viewer_ip", "created_at"]