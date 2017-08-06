from django.contrib import admin
from links.models import Category, Page

class PageInline(admin.TabularInline):
    model = Page
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    inlines = [PageInline]
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)
