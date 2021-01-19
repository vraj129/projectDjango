from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.files import File
import os

# Read this issue for more details why `uuid` is used

# Github Link:
# https://github.com/nesdis/djongo/issues/8

# Answer:
# https://github.com/nesdis/djongo/issues/8#issuecomment-723484705

# Create your models here
class Extra_User_Detail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_url = models.URLField()
    locale = models.CharField(default="en", max_length=10)


    def __str__(self):
        return self.user.username


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_url = models.URLField()
