from django.db import models
from django.utils.timezone import now
import uuid
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars  # or truncatewords
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from .utils import delete_realted_data


class Article(models.Model):
    # Shows which user has written the article
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)

    # File location
    file_location = models.CharField(
        max_length=255, default='templates/articles/')

    # Main title
    title = models.CharField(max_length=80)  # Try not to exceed 70

    # url
    url_title = models.SlugField(max_length=80,
                                 unique=True,
                                 db_index=True)  # Try not to exceed 70

    # total visitors, unique visitors
    # total_time_spent
    # indexing_count
    # index_increment_in_last_5_days
    # index bahut jaldi change hora h, means voh trending me h

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

    # Category
    category = models.CharField(max_length=511, blank=True)

    # Count views
    views_count = models.PositiveIntegerField(default=0)

    # weightage of Article(BigIntegerField)

    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#bigintegerfield
    # A 64-bit integer, much like an IntegerField except that it is guaranteed
    # to fit numbers from -9223372036854775808 to 9223372036854775807.
    # The default form widget for this field is a NumberInput
    weight = models.BigIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
        ]
    )

    # Date Modified
    date_modified = models.DateTimeField(auto_now=now)

    # Date Created
    date_created = models.DateTimeField(auto_now_add=now)

    def save(self, *args, **kwargs):
        print("Article saved, Jai Swaminarayan")
        super(Article, self).save(*args, **kwargs)

    # Bulk delete is defined `Article/admin.py`
    def delete(self, *args, **kwargs):
        delete_realted_data(self)
        super(Article, self).delete(*args, **kwargs)

    # def __str__(self):
    #     return (str(self.id) + " " +
    #             str(self.url_title) + " (" + str(self.meta_description) + ")")


class Hashtag(models.Model):
    hashtag_name = models.CharField(max_length=150)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)

    # So that case insensitive is taken into consideration
    def clean(self):
        if Hashtag.objects.filter(article_id=self.article_id).count()>=30:
            raise ValidationError('Only 30 hashtags allowed per article')
        # self.hashtag_name = self.hashtag_name.lower()

    def __str__(self):
        return (str(self.hashtag_name))


FAKE_INFO = 'FI'
HATE_SPEECH = 'HS'
HARRASMENT = 'HR'
ILLEGAL_SALE = 'IS'
NUDITY = 'ND'
SPAM = 'SP'
VIOLATION_OF_LAWS = 'VL'
OTHERS = 'OT'

REPORT_REASON = (
    (FAKE_INFO, 'Fake Information'),
    (HATE_SPEECH, 'Hate Speech'),
    (HARRASMENT, 'Harrasment'),
    (ILLEGAL_SALE, 'llegal Sale'),
    (NUDITY, 'Nudity'),
    (SPAM, 'Spam'),
    (VIOLATION_OF_LAWS, 'Violation of Laws'),
    (OTHERS, 'Others'),
)


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Use PROTECT as of now, RESTRICT is not supported in current version
    # RESTRICT: (introduced in Django 3.1)
    # Similar behavior as PROTECT that matches SQL's RESTRICT more accurately.
    # article_link = models.OneToOneField(Article, on_delete=models.RESTRICT)
    # article_link = models.OneToOneField(Article, on_delete=models.PROTECT)
    article_id = models.ForeignKey(Article, on_delete=models.PROTECT)

    user_id = models.ForeignKey(User, on_delete=models.PROTECT)

    # If ForeignKey duplicate fields are not inserted,
    # delete all migartions and try again
    # IF even after deleting all migrations, it gives an DB error,
    # Open database and drop the same table and try again

    reason = models.CharField(max_length=2,
                              choices=REPORT_REASON,
                              # default='green',
                              )

    brief_reason = models.TextField(blank=True, max_length=1023)

    @property
    def short_reason(self):
        return truncatechars(self.brief_reason, 280)
    solved_status = models.BooleanField(default=False)

    # Date Created
    date_created = models.DateTimeField(auto_now_add=now)

    # unique constraint by combining 2 keys
    class Meta:
        unique_together = [['article_id', 'user_id']]


MOBILE = 'M'
TABLET = 'T'
PC = 'P'
NONE = 'N'

DEVICE_AGENT = (
    (MOBILE, 'Mobile'),
    (TABLET, 'Tablet'),
    (PC, 'PC'),
    (NONE, 'None'),
)


class Viewer(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    ip_address = models.GenericIPAddressField()

    device_agent = models.CharField(max_length=1, choices=DEVICE_AGENT)
    is_touch_capable = models.BooleanField(default=True)
    is_bot = models.BooleanField(default=False)

    browser_family = models.CharField(max_length=63)
    browser_version = models.CharField(max_length=42, blank=True)

    os_family = models.CharField(max_length=63)
    os_version = models.CharField(max_length=42, blank=True)

    device_agent_family = models.CharField(max_length=73)

    date_viewed = models.DateTimeField(auto_now_add=now)

    class Meta:
        unique_together = [['article_id', 'user_id', 'ip_address']]

# # Make this Model also (shayad jarur padse):
# trending_articles
