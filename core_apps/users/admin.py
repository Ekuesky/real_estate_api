from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import UserChangeForm, UserCreationForm
from core_apps.profiles.models import Profile
from django.utils.html import  format_html
from .forms import ProfileForm

User = get_user_model()
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    form = ProfileForm
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    readonly_fields = ['avatar_preview', 'slug', ]

    def avatar_preview(self, instance):
        if instance.avatar:
            return format_html('<img src="{}" width="300" height="300" style="object-fit: cover;" />', instance.avatar.url)
        return "No avatar"
    avatar_preview.short_description = "Preview"

    fieldsets = (
        ('', {'fields': ('avatar_preview', 'avatar')}),
        ('', {'fields': ('gender', 'occupation', 'bio', 'phone_number', 'country_of_origin','city_of_origin','report_count',
                         'reputation', 'slug')}),
    )


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
            width, height = 80, 80  # Set desired width and height
            return format_html(
                '<img src="{}" width="{}" height="{}" style="border-radius: 50%;" />',  # No leading slash
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

