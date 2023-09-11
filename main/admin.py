from django.contrib import admin
from .models import Article, Profile, Comment, Report

admin.site.register(Article)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Report)
