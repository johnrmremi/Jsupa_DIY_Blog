from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

# Create your models here.
from django.contrib.auth.models import User


class Comment(models.Model):
    """Model representing a post comment."""
    content = models.TextField(max_length=1000, help_text='Enter the comment of a post')
    post = models.ForeignKey('Post', on_delete=models.RESTRICT, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_comment = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['date_of_comment']

    def display_comment_reduced(self):
        """Create a string for the commet. This is required to display the first 10 words of blog comment in the admin interface."""
        if len(self.content) > 75:
            self.content = self.content[:75]
            return self.content + ' ...'
        return self.content

    display_comment_reduced.short_description = 'Comment'

    def display_post_reduced(self):
        """Create a string for the post. This is required to display the first 10 words of blog post in the admin interface."""
        test  =  str(self.post)
        if len(test) > 10:
            test = test[:10]
            return test + ' ...'
        return test

    display_post_reduced.short_description = 'Post'

    def __str__(self):
        """String for representing the Model object."""
        return self.content

class Post(models.Model):
    """Model representing a post."""
    title = models.CharField(max_length=200)

    # Foreign Key used because post can only have one (blogger)author, but bloggers can have multiple posts
    # Blogger as a string rather than object because it hasn't been declared yet in the file
    blogger = models.ForeignKey('Blogger', on_delete=models.SET_NULL, null=True)

    content = models.TextField(max_length=1000, help_text='Enter the content of a post')
    date_of_post = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-date_of_post']

        # Defining the permission to allow loggin in bloggers to view their blogs.
        permissions = (("can_view_blogs", "View blogs as blogger"),)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this post."""
        return reverse('blog-detail', args=[str(self.id)])


class Blogger(models.Model):
    """Model representing an author(blogger)."""
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(max_length=500, help_text='Enter the biography about the blogger')

    class Meta:
        ordering = ['author']

    def display_bio_reduced(self):
        """Create a string for the bio. This is required to display the first 100 words of blogger biography in the admin interface."""
        if len(self.bio) > 100:
            self.bio = self.bio[:100]
            return self.bio + ' ...'
        return self.bio

    display_bio_reduced.short_description = 'Bio'


    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('blogger-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.author}'
