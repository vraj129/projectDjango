from django.contrib import admin
from .models import Extra_User_Detail
from django.contrib import messages

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


# admin.site.disable_action('delete_selected')
admin.site.register(Extra_User_Detail, Extra_User_DetailAdmin)
