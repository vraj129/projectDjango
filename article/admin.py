from django.contrib import admin
from django.db import models
from .models import Article, Report, Viewer, Hashtag
from django.contrib import messages
from django.utils.translation import ngettext
from django.forms import Textarea
from .utils import delete_realted_data
from django.db.models import F, Count, Window, Min, Q


# https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.StackedInline
class HashtagInline(admin.TabularInline):
    model = Hashtag


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        HashtagInline,
    ]

    list_display = ('id', 'user_id',
                    'url_title',
                    'publish_status', 'allow_comments', 'views_count',
                    'weight',
                    'date_modified', 'date_created')

    ordering = ['-date_created']

    actions = [
        'publish_selected_articles', 'archieve_selected_articles',
        'allow_comments', 'disable_comments',
        'custom_delete',

        # If we write | admin.site.disable_action('delete_selected') | anywhere
        # Below line should be removed from comment
        # 'delete_selected',
    ]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 40})},
    }

    def get_actions(self, request):
        actions = super(ArticleAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    # Single delete which is done from object view in Admin Panel
    # is defined `Article/models.py`
    def custom_delete(self, request, queryset):
        for obj in queryset:
            delete_realted_data(obj)
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 Article entry was"
        else:
            message_bit = "%s Articles were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)

    custom_delete.short_description = "Delete selected Articles"

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


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'article_id',  # fk
                    'user_id',  # fk
                    'reason',
                    # 'short_reason',
                    'solved_status',
                    'date_created',
                    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            count_by_article=Window(
                expression=Count('article_id', filter=Q(solved_status=False)),
                partition_by=F('article_id')
            ),
            count_by_article_and_reason=Window(
                expression=Count('article_id', filter=Q(solved_status=False)),
                partition_by=[F('article_id'), F('reason')],
            ),
            earliest_report_by_article=Window(
                expression=Min('date_created', filter=Q(solved_status=False)),
                partition_by=[F('article_id')],
            ),
            earliest_report_by_article_and_reason=Window(
                expression=Min('date_created', filter=Q(solved_status=False)),
                partition_by=[F('article_id'), F('reason')],
            ),
        ).order_by('solved_status', '-count_by_article',
                   'earliest_report_by_article', 'article_id',
                   '-count_by_article_and_reason', 'earliest_report_by_article_and_reason',
                   'reason', 'date_created')
        # return super().get_queryset(request).annotate(
        #     count_by_article=Window(
        #         expression=Count('*'),
        #         partition_by=F('article_id')
        #     ),
        #     count_by_article_and_reason=Window(
        #         expression=Count('*'),
        #         partition_by=[F('article_id'), F('reason')],
        #     ),
        #     earliest_report_by_article=Window(
        #         expression=Min('date_created'),
        #         partition_by=[F('article_id')],
        #     ),
        #     earliest_report_by_article_and_reason=Window(
        #         expression=Min('date_created'),
        #         partition_by=[F('article_id'), F('reason')],
        #     ),
        # ).order_by('solved_status', '-count_by_article', 'earliest_report_by_article', 'article_id',
        #            '-count_by_article_and_reason', 'earliest_report_by_article_and_reason',
        #            'reason', 'date_created')

    actions = [
        'mark_as_solved',
        'mark_as_unsolved',
        # 'show_artist_count',
    ]

    def mark_as_solved(self, request, queryset):
        updated = queryset.update(solved_status=True)
        self.message_user(request, ngettext(
            '%d article was successfully marked as Solved.',
            '%d articles were successfully marked as Solved.',
            updated,
        ) % updated, messages.SUCCESS)

    mark_as_solved.short_description = "Mark as Solved"

    def mark_as_unsolved(self, request, queryset):
        updated = queryset.update(solved_status=False)
        self.message_user(request, ngettext(
            '%d article was marked as NOT Solved.',
            '%d articles were marked as NOT Solved.',
            updated,
        ) % updated, messages.SUCCESS)

    mark_as_unsolved.short_description = "Mark as NOT Solved"


# to sort top groups, get highest weightage `Article`
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'hashtag_name', 'article_id',
                    )


class ViewerAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'article_id', 'user_id', 'ip_address',
                    'device_agent', 'is_touch_capable', 'is_bot',
                    'browser_family', 'browser_version',
                    'os_family', 'os_version',
                    'device_agent_family',
                    'date_viewed'
                    )


# Register your models here.
admin.site.register(Viewer, ViewerAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Report, ReportAdmin)
# admin.site.register(Category)
admin.site.register(Hashtag, HashtagAdmin)
