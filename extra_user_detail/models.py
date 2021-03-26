from django.db import models
import uuid
from django.contrib.auth.models import User
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


# class Item(models.Model):
#     id = models.UUIDField(primary_key=True,
#                           default=uuid.uuid4,
#                           editable=False)
#     image_url = models.URLField()

# this_table_id(auto generated)

# article_id
# user_id
# read_status
# saved_status
# engagement_time
class Article_Interaction(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
