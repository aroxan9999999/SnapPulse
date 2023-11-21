from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, UserRelation


class UserRelationInline(admin.TabularInline):
    model = UserRelation
    fk_name = 'follower'
    extra = 1
    verbose_name = 'Relationship'
    verbose_name_plural = 'Relationships'
    show_change_link = True


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'get_profile_pic', 'bio', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    inlines = (UserRelationInline,)  # This will handle the following relationships
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'get_profile_pic', 'profile_pic', 'bio', 'blocked_users')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    readonly_fields = ('get_profile_pic',)

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" width="150" height="150" style="border-radius:50%; border:3px solid #FF69B4;/>', obj.profile_pic.url)
        return "-"

    get_profile_pic.short_description = 'Profile Picture'

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
