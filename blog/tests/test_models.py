from django.test import TestCase

from blog.models import Blogger, Blog, Comment
import datetime
from django.contrib.auth.models import User # Required to assign User as a Blogger

class BloggerModelTest(TestCase):
    """ Unit test fot Blogger model """
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        Blogger.objects.create(author=test_user1, bio='John Davison Rockefeller Sr. was an American business magnate and philanthropist. He is widely considered the wealthiest American of all time and the richest person in modern history. ')

    def test_author_label(self):
        blogger = Blogger.objects.get(id=1)
        field_label = blogger._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_bio_label(self):
        blogger = Blogger.objects.get(id=1)
        field_label = blogger._meta.get_field('bio').verbose_name
        self.assertEqual(field_label, 'bio')

    def test_bio_max_length(self):
        blogger = Blogger.objects.get(id=1)
        max_length = blogger._meta.get_field('bio').max_length
        self.assertEqual(max_length, 500)

    def test_bio_help_text(self):
        blogger = Blogger.objects.get(id=1)
        help_text = blogger._meta.get_field('bio').help_text
        self.assertEqual(help_text, 'Enter your bio details here.')
    
    def test_display_shor_bio_description(self):
        blogger = Blogger.objects.get(id=1)
        bio_len = len(blogger.bio)
        if bio_len > 100:
            bio_len = 100
            self.assertEqual(bio_len, 100)
        else:
            self.assertEqual(bio_len, len(blogger.bio))

    def test_object_name_is_blogger_author_name(self):
        blogger = Blogger.objects.get(id=1)
        expected_object_name = f'{blogger.author}'
        self.assertEqual(str(blogger), expected_object_name)

    def test_get_absolute_url(self):
        blogger = Blogger.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(blogger.get_absolute_url(), '/blog/blogger/1')

class BlogModelTest(TestCase):
    """ Unit test for Blog model """
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        blogger1 = Blogger.objects.create(author=test_user1, bio='John Davison Rockefeller Sr. was an American business magnate and philanthropist. He is widely considered the wealthiest American of all time and the richest person in modern history. ')
        today = datetime.date.today()
        Blog.objects.create(name='Why Africa is rich in minerals but its people are the poorest?', blogger=blogger1, description='The great reason and cause for that is poor education system, which cause the people to lack awareness of their values in this planent and the whole universe at large', post_date=today)
    
    def test_name_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_blogger_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('blogger').verbose_name
        self.assertEqual(field_label, 'blogger')

    def test_description_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_description_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)

    def test_description_help_text(self):
        blog = Blog.objects.get(id=1)
        help_text = blog._meta.get_field('description').help_text
        self.assertEqual(help_text, 'Enter you blog text here.')

    def test_post_date_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('post_date').verbose_name
        self.assertEqual(field_label, 'post date')

    def test_defaul_tpost_date(self):
        blog = Blog.objects.get(id=1)
        default_post_date = blog.post_date
        self.assertEqual(default_post_date, datetime.date.today())

    def test_object_name_is_blog_name(self):
        blog = Blog.objects.get(id=1)
        expected_object_name = f'{blog.name}'
        self.assertEqual(str(blog), expected_object_name)

    def test_get_absolute_url(self):
        blog = Blog.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(blog.get_absolute_url(), '/blog/blog/1')


class CommentModelTest(TestCase):
    """ Unit test for Comment model """
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1X<ISRUkw+tuK')
        blogger1 = Blogger.objects.create(author=test_user1, bio='John Davison Rockefeller Sr. was an American business magnate and philanthropist. He is widely considered the wealthiest American of all time and the richest person in modern history. ')
        today = datetime.date.today()
        blog1 = Blog.objects.create(name='Why Africa is rich in minerals but its people are the poorest?', blogger=blogger1, description='The great reason and cause for that is poor education system, which cause the people to lack awareness of their values in this planent and the whole universe at large', post_date=today)
        Comment.objects.create(description='Yaah that is true, but also africans are so lazzy people to think about their future', blog=blog1, author=test_user2, post_date=today)

    def test_description_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_description_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)

    def test_description_help_text(self):
        comment = Comment.objects.get(id=1)
        help_text = comment._meta.get_field('description').help_text
        self.assertEqual(help_text, 'Enter comment about blog here.')

    def test_blog_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('blog').verbose_name
        self.assertEqual(field_label, 'blog')

    def test_author_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_post_date_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('post_date').verbose_name
        self.assertEqual(field_label, 'post date')

    def test_post_date_auto_now_add(self):
        comment = Comment.objects.get(id=1)
        auto_now_add = comment._meta.get_field('post_date').auto_now_add
        self.assertTrue(auto_now_add, True)

    def test_display_short_comment_description(self):
        comment = Comment.objects.get(id=1)
        description_length = len(comment.description)
        if description_length > 75:
            description_length = 75
            self.assertEqual(description_length, 75)
        else:
            self.assertEqual(description_length, len(comment.description))

    def test_display_short_blog_name(self):
        comment = Comment.objects.get(id=1)
        blog_length = len(str(comment.blog))
        if blog_length > 10:
            blog_length = 10
            self.assertEqual(blog_length, 10)
        else:
            self.assertEqual(blog_length, len(comment.blog))

    def test_object_name_is_comment_description(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = f'{comment.description}'
        self.assertEqual(str(comment), expected_object_name)