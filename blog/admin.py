from django.contrib import admin

# Register your models here.

from .models import Post, Blogger, Comment

# admin.site.register(Post)
# admin.site.register(Blogger)
# admin.site.register(Comment)

class PostInline(admin.TabularInline):
    model = Post
    extra = 0
# Define the admin class
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('author', 'display_bio_reduced')
    inlines = [PostInline]

# Register the admin class with the associated model
admin.site.register(Blogger, BloggerAdmin)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

# Register the Admin classes for Post using the decorator
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'blogger', 'date_of_post')
    list_filter = ('date_of_post','blogger')
    inlines = [CommentInline]

# Register the Admin classes for Comment using the decorator
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('display_comment_reduced', 'display_post_reduced', 'date_of_comment', 'author')
    list_filter = ('date_of_comment', 'post')
 

