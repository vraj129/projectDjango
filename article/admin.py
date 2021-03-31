from django.contrib import admin
from django.db import models
from .models import Article, Report, Viewer, Hashtag
from django.contrib import messages
from django.utils.translation import ngettext
from django.forms import Textarea


# https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.StackedInline
class HashtagInline(admin.TabularInline):
    model = Hashtag


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        HashtagInline,
    ]

    list_display = ('id', 'url_title',
                    'publish_status', 'allow_comments', 'views_count',
                    'weight',
                    'date_modified', 'date_created')

    ordering = ['-date_created']

    actions = [
        'publish_selected_articles', 'archieve_selected_articles',
        'allow_comments', 'disable_comments',

        # If we write | admin.site.disable_action('delete_selected') | anywhere
        # Below line should be removed from comment
        # 'delete_selected',
    ]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 40})},
    }

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
                    'reason', 'short_reason',
                    'solved_status',
                    'date_created',
                    )

    # ordering = ['solved_status', 'date_created']
    # highetst count of artcile link
    # count of reason

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

    # def get_queryset(self, request):
    #     qs = super(ReportAdmin, self).get_queryset(request)
    #     # return qs.filter(user__username__icontains="jo")
    #     return qs.annotate(num_user=Count('user'))
    #     # return qs.annotate(Count('article_link'))
    #     # if request.user.is_superuser:
    #     #     return qs

    # def queryset(self, request):
    # def get_queryset(self, request):
    #     qs = super(ReportAdmin, self).get_queryset(request)
    #     # return qs.filter(user__username__icontains="jo")
    #     return qs.annotate(user_count=Count('user'))

    # def show_user_count(self, inst):
    #     return inst.user_count
    # show_user_count.admin_order_field = 'user_count'

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
