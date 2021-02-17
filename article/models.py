from django.db import models
from django.utils.timezone import now


# Create your models here.
class Article(models.Model):
    # File location
    file_location = models.CharField(max_length=255)

    # Main title
    title = models.CharField(max_length=80)  # Try not to exceed 70

    # url
    url_title = models.CharField(max_length=80)  # Try not to exceed 70

    # Meta tags
    meta_keywords = models.TextField(blank=True)
    meta_current_page_url = models.CharField(max_length=511, blank=True, null=True)
    meta_description = models.CharField(max_length=165, blank=True)  # Try not to exceed 155
    meta_image_url = models.CharField(max_length=200, blank=True)

    # Images location
    images = models.TextField(blank=True, null=True)

    # Facebook sharing link
    facebook_sharing_link = models.CharField(max_length=1023, blank=True)

    # Publish Status
    publish_status = models.BooleanField(default=False)

    # All Categories to which blog belongs Pending and check wordpress

    # Count views
    views_count = models.PositiveIntegerField(default=0)

    # Date Modified
    date_modified = models.DateTimeField(auto_now=now)

    # Date Created
    date_created = models.DateTimeField(auto_now_add=now)

    def __str__(self):
        return (str(self.id) + " " +
                str(self.url_title) + " (" + str(self.meta_description) + ")")
