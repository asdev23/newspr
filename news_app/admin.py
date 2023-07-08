from django.contrib import admin
from .models import News, Category, Contact, Comment

# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','slug','publish_time','status']
    list_filter = ['status','create_time','publish_time']
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'publish_time'
    search_fields = ['title','body']
    ordering = ['title','body']

@admin.register(Category)
class Categoryadmin(admin.ModelAdmin):
    list_display = ['id','name']
    ordering=['id']

admin.site.register(Contact)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','body','created_time','active']
    list_filter = ['user','created_time','active']
    search_fields = ['user','body']
    actions = ['disable_comments','active_comments']

    def disable_comments(self,request,queryset):
        queryset.update(active=False)

    def active_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Comment, CommentAdmin)