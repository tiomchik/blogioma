# Generated by Django 4.2.1 on 2023-06-27 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nickname', models.CharField(max_length=20, unique=True, verbose_name='Ник')),
                ('pfp', models.ImageField(blank=True, upload_to='get_username/', verbose_name='Аватарка')),
                ('email', models.CharField(max_length=320, unique=True, verbose_name='Email')),
                ('password', models.CharField(max_length=25, verbose_name='Пароль')),
                ('join_date', models.DateField(auto_now_add=True, verbose_name='Дата регистрации')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headling', models.CharField(max_length=30, verbose_name='Заголовок')),
                ('full_text', models.TextField(verbose_name='Текст')),
                ('pub_date', models.DateTimeField(verbose_name='Дата публикации')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.profile', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]
