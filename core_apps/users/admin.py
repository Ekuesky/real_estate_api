from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import UserChangeForm, UserCreationForm
from core_apps.profiles.models import Profile
from django.utils.html import  format_html

User = get_user_model()
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'
    fk_name = 'user'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = (ProfileInline,)

    list_display = [
        "pkid",
        "id",
        "email",
        "avatar",
        "first_name",
        "last_name",
        "username",
        "is_superuser",
        "get_gender",
        "get_occupation",

    ]
    list_display_links = ["pkid", "id", "email", "username"]
    search_fields = ["email", "first_name", "last_name", "username"]
    ordering = ["pkid"]
    list_select_related = ('profile',)

    def avatar(self, instance):
        if instance.profile.avatar:
            width, height = 80, 100  # Set desired width and height
            return format_html(
                '<img src="{}" width="{}" height="{}" />',  # No leading slash
                instance.profile.avatar.url, width, height
            )
        return None
    def get_gender(self, instance):
        return instance.profile.gender

    get_gender.short_description = 'Gender'

    def get_occupation(self, instance):
        return instance.profile.occupation

    get_occupation.short_description = 'Occupation'

    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "username")}),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)
