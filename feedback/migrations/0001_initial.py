# Generated by Django 4.2.3 on 2024-04-23 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial')
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('Banned advertising', 'Banned advertising (casino, porn-sites, etc.)'), ('Banned content', 'Content that is unpleasant to some readers (shock content, etc.), illegal or tragic content'), ('18+ content', '18+ content'), ('Scam', 'Scam'), ('Swearing', 'Swearing'), ('Copyright infringement', 'Copyright infringement'), ('Data/media leakage', 'Data/media leakage (paid courses, candid photos, etc.)')], max_length=110, verbose_name='Reason')),
                ('desc', models.CharField(blank=True, max_length=200, null=True, verbose_name='Description')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
        ),
    ]
