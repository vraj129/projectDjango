from django.db import models
from django.utils.timezone import now


class Group(models.Model):
    category_name = models.CharField(max_length=63, primary_key=True)

    # So that case insensitive is taken into consideration
    def clean(self):
        self.category_name = self.category_name.capitalize()

    def __str__(self):
        return (str(self.category_name))


class Article(models.Model):
    # File location
    file_location = models.CharField(max_length=255)

    # Main title
    title = models.CharField(max_length=80)  # Try not to exceed 70

    # url
    url_title = models.CharField(max_length=80)  # Try not to exceed 70

    # Featured Image
    featured_image = models.ImageField(upload_to='article_pictures',
                                       blank=True)

    # Meta tags
    meta_keywords = models.TextField(blank=True)
    meta_description = models.CharField(max_length=165,
                                        blank=True)  # Try not to exceed 155

    # Images location
    images = models.TextField(blank=True, null=True)

    # Publish Status
    publish_status = models.BooleanField(default=False)

    # Publish Status
    allow_comments = models.BooleanField(default=True)

    # Categories
    categories = models.CharField(max_length=511, blank=True)

    # Count views
    views_count = models.PositiveIntegerField(default=0)

    # Date Modified
    date_modified = models.DateTimeField(auto_now=now)

    # Date Created
    date_created = models.DateTimeField(auto_now_add=now)

    def __str__(self):
        return (str(self.id) + " " +
                str(self.url_title) + " (" + str(self.meta_description) + ")")
