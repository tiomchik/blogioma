# Generated by Django 4.2.11 on 2024-04-27 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_rename_article_report_reported_article'),
        ('articles', '0002_alter_article_options_remove_article_reports_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='reports',
            field=models.ManyToManyField(blank=True, to='feedback.report'),
        ),
    ]
