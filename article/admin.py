from django.contrib import admin
from .models import Article, Group
from django.contrib import messages
from django.utils.translation import ngettext


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'url_title',
                    'publish_status', 'allow_comments', 'views_count',
                    'date_modified', 'date_created')

    ordering = ['-date_modified']

    actions = [
        'publish_selected_articles', 'archieve_selected_articles',
        'allow_comments', 'disable_comments',

        # If we write | admin.site.disable_action('delete_selected') | anywhere
        # Below line should be removed from comment
        # 'delete_selected',
    ]

    def publish_selected_articles(self, request, queryset):
        updated = queryset.update(publish_status=True)
        self.message_user(request, ngettext(
            '%d article was successfully marked as Published.',
            '%d articles were successfully marked as Published.',
            updated,
        ) % updated, messages.SUCCESS)
        # messages.success(request,
        #                  "Selected Record(s) Marked as Published")

    def archieve_selected_articles(self, request, queryset):
        updated = queryset.update(publish_status=False)
        self.message_user(request, ngettext(
            '%d article was successfully marked as Archieved.',
            '%d articles were successfully marked as Archieved.',
            updated,
        ) % updated, messages.SUCCESS)
        # messages.success(request,
        #                  "Selected Record(s) Marked as Archieve")

    def allow_comments(self, request, queryset):
        updated = queryset.update(allow_comments=True)
        self.message_user(request, ngettext(
            'Allowed Comments on %d Article',
            'Allowed Comments on %d Articles',
            updated,
        ) % updated, messages.SUCCESS)
        # messages.success(request,
        #                  "Comments allowed on Selected Record(s)")

    def disable_comments(self, request, queryset):
        updated = queryset.update(allow_comments=False)
        self.message_user(request, ngettext(
            'Disabled Comments on %d Article',
            'Disabled Comments on %d Articles',
            updated,
        ) % updated, messages.SUCCESS)
        # messages.success(request,
        #                  "Comments disabled on Selected Record(s)")

    publish_selected_articles.short_description = "Mark as published"
    archieve_selected_articles.short_description = "Mark as Archieved"
    allow_comments.short_description = "Allow Comments"
    disable_comments.short_description = "Disable Comments"

    # Writing this will add_action globally
    # admin.site.add_action(disable_comments,
    #                       "Disable comments")


# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Group)
