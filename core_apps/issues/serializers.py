import logging

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import serializers

from core_apps.common.models import ContentView  # Import the ContentView model for view count calculation
from .emails import send_resolution_email  # Import the email function to send resolution notifications
from .models import Issue  # Import the Issue model

logger = logging.getLogger(__name__)  # Set up a logger for error tracking


# Define a serializer for Issue objects
class IssueSerializer(serializers.ModelSerializer):
    # Read-only fields to display related data
    apartment_unit = serializers.ReadOnlyField(source="apartment.unit_number")
    reported_by = serializers.ReadOnlyField(source="reported_by.get_full_name")
    assigned_to = serializers.ReadOnlyField(source="assigned_to.get_full_name")
    view_count = serializers.SerializerMethodField()  # Add a custom method to get the view count

    # Define the fields to be included in the serializer
    class Meta:
        model = Issue
        fields = [
            "id",
            "apartment_unit",
            "reported_by",
            "assigned_to",
            "title",
            "description",
            "status",
            "priority",
            "view_count",
        ]

    # Define the custom method to get the view count for an issue
    def get_view_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)  # Get the ContentType for the Issue model
        return ContentView.objects.filter(  # Query the ContentView model
            content_type=content_type, object_id=obj.pkid  # Filter by content type and object ID
        ).count()  # Count the number of views


# Define a serializer to handle updates to Issue status
class IssueStatusUpdateSerializer(serializers.ModelSerializer):
    # Read-only fields to display related data
    apartment = serializers.ReadOnlyField(source="apartment.unit_number")
    reported_by = serializers.ReadOnlyField(source="reported_by.get_full_name")
    resolved_by = serializers.ReadOnlyField(source="assigned_to.get_full_name")

    # Define the fields to be included in the serializer
    class Meta:
        model = Issue
        fields = [
            "title",
            "description",
            "apartment",
            "reported_by",
            "status",
            "resolved_by",
            "resolved_on",
        ]

    # Override the update method to handle status changes
    def update(self, instance: Issue, validated_data: dict) -> Issue:
        # Check if the status is changing to RESOLVED
        if (
            validated_data.get("status") == Issue.IssueStatus.RESOLVED
            and instance.status != Issue.IssueStatus.RESOLVED
        ):
            # Set the resolved_on date to the current date
            instance.resolved_on = timezone.now().date()
            instance.save()  # Save the updated issue
            send_resolution_email(instance)  # Send a resolution notification email
        # Call the superclass update method to handle other field updates
        return super().update(instance, validated_data)