# Generated by Django 3.0.5 on 2021-03-07 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_remove_article_meta_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='facebook_sharing_link',
        ),
    ]
