# Generated by Django 3.0.5 on 2021-03-30 17:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_location', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=80)),
                ('url_title', models.CharField(db_index=True, max_length=80, unique=True)),
                ('featured_image', models.ImageField(blank=True, upload_to='article_pictures')),
                ('meta_keywords', models.TextField(blank=True)),
                ('meta_description', models.CharField(blank=True, max_length=165)),
                ('images', models.TextField(blank=True, null=True)),
                ('publish_status', models.BooleanField(default=False)),
                ('allow_comments', models.BooleanField(default=True)),
                ('categories', models.CharField(blank=True, max_length=511)),
                ('views_count', models.PositiveIntegerField(default=0)),
                ('weight', models.BigIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=63)),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('device_agent', models.CharField(choices=[('M', 'Mobile'), ('T', 'Tablet'), ('P', 'PC'), ('N', 'None')], max_length=1)),
                ('is_touch_capable', models.BooleanField(default=True)),
                ('is_bot', models.BooleanField(default=False)),
                ('browser_details', models.CharField(max_length=255)),
                ('os_details', models.CharField(max_length=255)),
                ('device_agent_family', models.CharField(max_length=73)),
                ('date_viewed', models.DateTimeField(auto_now_add=True)),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='article.Article')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('article_id', 'user_id', 'ip_address')},
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reason', models.CharField(choices=[('FI', 'Fake Information'), ('HS', 'Hate Speech'), ('HR', 'Harrasment'), ('IS', 'llegal Sale'), ('ND', 'Nudity'), ('SP', 'Spam'), ('VL', 'Violation of Laws'), ('OT', 'Others')], max_length=2)),
                ('brief_reason', models.TextField(blank=True, max_length=1023)),
                ('solved_status', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='article.Article')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('article_id', 'user_id')},
            },
        ),
    ]
