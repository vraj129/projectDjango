from django.contrib import admin
from .models import Extra_User_Detail, Article_Interaction
from django.contrib import messages
from django.utils.translation import ngettext

# Register your models here.


class Extra_User_DetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'locale', 'verified_profile')
    actions = [
        'mark_as_verified_users',
        'mark_as_non_verified_users',

        # If we write | admin.site.disable_action('delete_selected') | anywhere
        # Below line should be removed from comment
        # 'delete_selected'
    ]

    def mark_as_verified_users(modeladmin, request, queryset):
        queryset.update(verified_profile=True)
        messages.success(request,
                         "Selected Record(s) Marked as Verified Accounts")

    def mark_as_non_verified_users(modeladmin, request, queryset):
        queryset.update(verified_profile=False)
        messages.success(request,
                         "Selected Record(s) Marked as Non-Verified Accounts")

    # admin.site.add_action(mark_as_verified_users,
    #                       "Mark as Verified")


class Article_InteractionAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_id', 'article_id',
                    'read_status', 'saved',
                    'engagement_time'
                    )
    ordering = ['-engagement_time', '-read_status', '-saved']

    actions = [
        'mark_as_read',
        'mark_as_unread',
        'mark_as_saved',
        'mark_as_unsaved',
    ]

    def mark_as_read(self, request, queryset):
        updated = queryset.update(read_status=True)
        self.message_user(request, ngettext(
            '%d Record was marked as Read.',
            '%d Records were marked as Read.',
            updated,
        ) % updated, messages.SUCCESS)

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(read_status=False)
        self.message_user(request, ngettext(
            '%d Record was marked as Unread.',
            '%d Records were marked as Unread.',
            updated,
        ) % updated, messages.SUCCESS)

    def mark_as_saved(self, request, queryset):
        updated = queryset.update(saved=True)
        self.message_user(request, ngettext(
            '%d Record was marked as Read.',
            '%d Records were marked as Read.',
            updated,
        ) % updated, messages.SUCCESS)

    def mark_as_unsaved(self, request, queryset):
        updated = queryset.update(saved=False)
        self.message_user(request, ngettext(
            '%d Record was marked as Saved.',
            '%d Records were marked as Unsaved.',
            updated,
        ) % updated, messages.SUCCESS)

    mark_as_read.short_description = "Mark as Read"
    mark_as_unread.short_description = "Mark as NOT Read"
    mark_as_saved.short_description = "Mark as Saved"
    mark_as_unsaved.short_description = "Mark as NOT Saved"


# admin.site.disable_action('delete_selected')
admin.site.register(Extra_User_Detail, Extra_User_DetailAdmin)
admin.site.register(Article_Interaction, Article_InteractionAdmin)
