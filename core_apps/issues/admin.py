from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from core_apps.common.admin import ContentViewInline  # Import the inline admin class for ContentViews
from core_apps.common.models import ContentView  # Import the ContentView model
from .models import Issue  # Import the Issue model

# Register the Issue model with the admin interface
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    # Define the fields to display in the list view
    list_display = [
        "id",
        "apartment",
        "reported_by",
        "assigned_to",
        "status",
        "priority",
        "get_total_views",  # Add a custom method to display the total views
    ]

    # Define the fields that are clickable links in the list view
    list_display_links = ["id", "apartment"]

    # Define the fields to filter the list view by
    list_filter = ["status", "priority"]

    # Define the fields to search within the list view
    search_fields = ["apartment__unit_number", "reported_by__first_name"]

    # Define the default ordering of the list view
    ordering = ["-created_at"]

    # Define the fields that use autocomplete for easy selection
    autocomplete_fields = ["apartment", "reported_by", "assigned_to"]

    # Add the ContentViewInline class to display ContentViews related to each Issue
    inlines = [ContentViewInline]

    # Custom method to retrieve the total views for an Issue
    def get_total_views(self, obj):
        # Get the ContentType instance for the Issue model
        content_type = ContentType.objects.get_for_model(obj)
        # Filter ContentView objects based on content_type and object_id
        views = ContentView.objects.filter(
            content_type=content_type, object_id=obj.pkid  # Use pkid instead of pk
        ).count()
        return views

    # Set the short description for the custom method in the list view
    get_total_views.short_description = "Total Views"