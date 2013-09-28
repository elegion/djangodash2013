from django.contrib import admin

from wtl.wtlib import models as wtlib


class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class LibraryVersionInline(admin.StackedInline):
    model = wtlib.LibraryVersion


class LibraryAdmin(admin.ModelAdmin):
    inlines = [LibraryVersionInline]
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(wtlib.Language, LanguageAdmin)
admin.site.register(wtlib.Library, LibraryAdmin)
