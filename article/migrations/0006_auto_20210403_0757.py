# Generated by Django 3.1.7 on 2021-04-03 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20210403_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
