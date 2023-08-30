# Generated by Django 4.2.1 on 2023-07-03 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_profile_email_remove_profile_join_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='update',
            field=models.DateTimeField(default=None, null=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
    ]
