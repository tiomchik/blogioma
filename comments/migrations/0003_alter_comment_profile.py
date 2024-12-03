# Generated by Django 4.2.16 on 2024-12-02 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0002_alter_comment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
