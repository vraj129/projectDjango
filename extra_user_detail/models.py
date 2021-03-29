from django.db import models
import uuid
from django.contrib.auth.models import User
from article.models import Article
from django.db.models import IntegerField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now


# from django.core.files import File
# import os

# Read this issue for more details why `uuid` is used

# Github Link:
# https://github.com/nesdis/djongo/issues/8

# Answer:
# https://github.com/nesdis/djongo/issues/8#issuecomment-723484705


# Create your models here
class Extra_User_Detail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #  32 "chars unique id"
    # + 4 ".jpg"
    # +23 "media/profile_pictures/"
    # --------------------------
    # 59 (We are using 80 for safe side)
    image_url = models.CharField(max_length=80)
    locale = models.CharField(default="en", max_length=10)
    verified_profile = models.BooleanField(default=False)

    # def __str__(self):
    #     return str(self.user.email + " - " + self.user.username)


# this_table_id(auto generated)

# article_id
# user_id
# read_status
# saved_status
# engagement_time

class Article_Interaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.OneToOneField(User, on_delete=models.PROTECT)
    article_id = models.OneToOneField(Article, on_delete=models.PROTECT)

    # scroll kari ne last sudhi jase, tyare read_status True thase
    read_status = models.BooleanField(default=False)
    saved = models.BooleanField(default=False)

    # 0 being the lowest, 99 being the highest
    engagement_time = IntegerField(
        default=0,
        validators=[
            MaxValueValidator(99),
            MinValueValidator(0)
        ]
    )
    # aa page chele kyare open kari ne niche scroll karyu, khbr padi jase
    # Date Modified
    date_last_read = models.DateTimeField(auto_now=now)

    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#durationfield
    # DurationField

    # unique constraint by combining 2 keys
    class Meta:
        unique_together = [['user_id', 'article_id']]


# class Login_Detail(models.Model):
#     pass
#     login_details:(refer Article.models.Viewer)
#     login_ip
#     device_agent = models.CharField(max_length=1, choices=DEVICE_AGENT)
#     browser_details = models.CharField(max_length=255)
#     os_details = models.CharField(max_length=255)
#     device_agent_family = models.CharField(max_length=73)
#     TIMESTAMP
