from django.contrib import admin
from rango.models import Category, Page, UserProfile


admin.site.register(UserProfile)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'views', 'likes')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class PageAdmin(admin.ModelAdmin):
    # fields = ['category', 'url']
    list_display = ('title', 'category', 'url', 'views')


admin.site.register(Page, PageAdmin)
