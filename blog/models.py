from datetime import date
from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

# Create your models here.
from django.contrib.auth.models import User


class Comment(models.Model):
    """Model representing a blog comment."""
    description = models.TextField(max_length=1000, help_text='Enter comment about blog here.')
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['post_date']

    def display_short_comment_description(self):
        """Create a string for the commet desscription. This is required to display the first 75 words of blog comment description if exceeded that length."""
        if len(self.description) > 75:
            self.description = self.description[:75]
            return self.description + ' ...'
        return self.description

    display_short_comment_description.short_description = 'Comment'

    def display_short_blog_name(self):
        """Create a string for the blog name. This is required to display the first 10 words of blog name in the admin interface."""
        test  =  str(self.blog)
        if len(test) > 10:
            test = test[:10]
            return test + ' ...'
        return test

    display_short_blog_name.short_description = 'Post'

    def __str__(self):
        """String for representing the Model object."""
        return self.description

class Blog(models.Model):
    """Model representing a blog."""
    name = models.CharField(max_length=200)

    # Foreign Key used because blog can only have one (blogger)author, but bloggers can have multiple blogs
    # Blogger as a string rather than object because it hasn't been declared yet in the file
    blogger = models.ForeignKey('Blogger', on_delete=models.SET_NULL, null=True)

    description = models.TextField(max_length=1000, help_text='Enter you blog text here.')
    post_date = models.DateField(default=date.today)

    class Meta:
        ordering = ['-post_date']

        # Permission for loggeed in bloggers to view, update and delete their blogs.
        permissions = (("can_add_and_update_and_delete_blog", "View blogs as blogger"),)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this post."""
        return reverse('blog-detail', args=[str(self.id)])


class Blogger(models.Model):
    """Model representing a blogger(blog author)."""
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(max_length=500, help_text='Enter your bio details here.')

    class Meta:
        ordering = ['author']

    def display_shor_bio_description(self):
        """Create a string for the bio. This is required to display the first 100 words of blogger biography in the admin interface."""
        if len(self.bio) > 100:
            self.bio = self.bio[:100]
            return self.bio + ' ...'
        return self.bio

    display_shor_bio_description.short_description = 'Bio'


    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('blogger-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.author}'
