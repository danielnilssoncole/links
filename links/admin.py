from django.contrib import admin
from links.models import Category, Page, UserProfile

class PageInline(admin.TabularInline):
    model = Page
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    inlines = [PageInline]
    list_display = ('name', 'views', 'likes')
    search_fields = ['name']
    prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'views')
    search_fields = ['title']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'website')
    search_fields = ['email']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
