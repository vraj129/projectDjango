from django.db import models


# Create your models here.
class Article(models.Model):
    # Main title
    title = models.CharField(max_length=80)  # Try not to exceed 70

    # url
    url_title = models.CharField(max_length=80, unique=True)  # Try not to exceed 70

    # Meta tags
    meta_keywords = models.TextField()
    meta_current_page_url = models.CharField(max_length=511)
    meta_description = models.CharField(max_length=165)  # Try not to exceed 155
    meta_image_url = models.URLField(max_length=200)

    # File location
    file_location = models.CharField(max_length=255)

    # Images location
    images = models.TextField()

    # Facebook sharing link
    facebook_sharing_link = models.CharField(max_length=1023)

    def __str__(self):
        return str(self.title) + " (" + str(self.meta_description) + ")"
