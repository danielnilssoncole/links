from django.contrib import admin
from links.models import Category, Page

class PageInline(admin.TabularInline):
    model = Page
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    inlines = [PageInline]
    list_display = ('name',)
    search_fields = ['name']
    prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
    search_fields = ['title']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
