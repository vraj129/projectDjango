# Generated by Django 3.0.5 on 2021-03-06 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_remove_article_meta_current_page_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='meta_image_url',
        ),
    ]
