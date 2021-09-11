from django.contrib import admin

# Register your models here.

from .models import Blog, Blogger, Comment

from django import forms

# admin.site.register(Blog)
# admin.site.register(Blogger)
# admin.site.register(Comment)

class BlogInline(admin.TabularInline):
    model = Blog
    extra = 0
# Define the admin class



class BloggerAdmin(admin.ModelAdmin):
    list_display = ('author', 'display_shor_bio_description')
    inlines = [BlogInline]

# Register the admin class with the associated model
admin.site.register(Blogger, BloggerAdmin)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class BlogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['blogger'].required = True
        self.fields['post_date'].required = True

    class Meta:
        model = Blog
        fields = '__all__'

# Register the Admin classes for Blog using the decorator
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'blogger', 'post_date')
    list_filter = ('post_date','blogger')
    search_fields = ['name']
    inlines = [CommentInline]

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].required = True

    class Meta:
        model = Comment
        fields = '__all__'

# Register the Admin classes for Comment using the decorator
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('display_short_comment_description', 'display_short_blog_name', 'post_date', 'author')
    list_filter = ('post_date', 'blog')