from django.contrib import admin

from django.contrib import admin
from .models import Page, SnippetVariant, Test

admin.site.register(Page)
admin.site.register(SnippetVariant)
admin.site.register(Test)

