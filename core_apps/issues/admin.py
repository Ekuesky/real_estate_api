from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from core_apps.common.admin import ContentViewInline
from core_apps.common.models import ContentView
from .models import Issue
from core_apps.users.models import User
from django.db.models import Q
from django.forms import ModelForm
from .emails import send_resolution_email, send_issue_confirmation_email
from django.utils import timezone


class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if the fields exist before filtering
        if "assigned_to" in self.fields:
            self.fields["assigned_to"].queryset = User.objects.exclude(
                Q(is_superuser=True) | Q(profile__occupation="tenant") | Q(is_active=False)
            )

        if "reported_by" in self.fields:
            self.fields["reported_by"].queryset = User.objects.filter(
                Q(is_active=True) & (Q(is_superuser=True) | Q(is_staff=True) | Q(profile__occupation__iexact="tenant"))
            )


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "apartment",
        "reported_by",
        "assigned_to",
        "status",
        "priority",
        "get_total_views",
    ]
    list_display_links = ["id", "apartment"]
    list_filter = ["status", "priority"]
    search_fields = ["apartment__unit_number", "reported_by__first_name", "reported_by__last_name"]
    ordering = ["-created_at"]
    autocomplete_fields = ["apartment"]
    inlines = [ContentViewInline]
    readonly_fields = ["resolved_on"]
    form = IssueForm

    def has_change_permission(self, request, obj=None):
        # Interdire la modification si l'objet existe et son statut est RESOLVED
        if obj and obj.status == Issue.IssueStatus.RESOLVED:
            return False
        return super().has_change_permission(request, obj)

    def get_total_views(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        views = ContentView.objects.filter(
            content_type=content_type, object_id=obj.pkid
        ).count()
        return views

    def save_model(self, request, obj, form, change):
        is_new = not change
        if is_new:
            obj.status = Issue.IssueStatus.REPORTED  # Set the status to REPORTED for a new issue
            send_issue_confirmation_email(obj)
        elif 'status' in form.changed_data:
            if obj.status == Issue.IssueStatus.RESOLVED and form.initial['status'] != Issue.IssueStatus.RESOLVED:
                obj.resolved_on = timezone.now().date()
                obj.resolved_by = request.user
                send_resolution_email(obj)
        super().save_model(request, obj, form, change)

    get_total_views.short_description = "Total Views"