import blog
from django.test import TestCase, RequestFactory
from django.urls import reverse

from blog.models import Blogger, Comment, Blog
from django.contrib.auth.models import User
import datetime


class BloggerListViewTest(TestCase):
    @classmethod

    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1y<ISRUkw+tuK1')
        Blogger.objects.create(author=test_user1, bio='John Davison Rockefeller Sr. was an American business magnate and philanthropist. He is widely considered the wealthiest American of all time and the richest person in modern history. ')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/bloggers/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogger_list.html')


class BlogListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 8 blogs for pagination tests
        today = datetime.date.today()
        test_user1 = User.objects.create_user(username='testuser1', password='1y<ISRUkw+tuK1')

        test_blogger1= Blogger.objects.create(author=test_user1, bio='John Davison Rockefeller Sr. was an American business magnate and philanthropist. He is widely considered the wealthiest American of all time and the richest person in modern history. ')

        number_of_blogs = 8

        for blog_num in range(number_of_blogs):
           Blog.objects.create(name='Test Blog %s' % blog_num, blogger=test_blogger1, description='Test Blog %s Description' % blog_num, post_date=today)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['blog_list']), 5)

    def test_lists_all_blogs(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('blogs')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['blog_list']), 3)

from blog.views import BlogDetailView, BloggerDetailView
class BlogDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 8 blogs for pagination tests
        today = datetime.date.today()
        test_user1 = User.objects.create_user(username='testuser1', password='1y<ISRUkw+tuK1')

        test_blogger1= Blogger.objects.create(author=test_user1, bio='John Davison Rockefeller Sr. was an American business magnate and philanthropist. He is widely considered the wealthiest American of all time and the richest person in modern history. ')
        Blog.objects.create(name='Test Blog 1', blogger=test_blogger1, description='Test Blog 1 Description', post_date=today)

    def test_view_url_exists_at_desired_location(self):
        self.factory = RequestFactory()
        blog = Blog.objects.get(id=1)
        request = self.factory.get('/blog/blog')
        response = BlogDetailView.as_view()(request, pk=blog.id)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        blog = Blog.objects.get(id=1)
        response = self.client.get(reverse('blog-detail', kwargs={'pk':blog.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        blog = Blog.objects.get(id=1)
        response = self.client.get(reverse('blog-detail', kwargs={'pk':blog.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_detail.html')

class BloggerDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 8 blogs for pagination tests
        test_user1 = User.objects.create_user(username='testuser1', password='1y<ISRUkw+tuK1')

        Blogger.objects.create(author=test_user1, bio='John Davison Rockefeller Sr. was an American business magnate and philanthropist. He is widely considered the wealthiest American of all time and the richest person in modern history. ')

    def test_view_url_exists_at_desired_location(self):
        self.factory = RequestFactory()
        blogger = Blogger.objects.get(id=1)
        request = self.factory.get('/blog/blogger')
        response = BloggerDetailView.as_view()(request, pk=blogger.id)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        blogger = Blogger.objects.get(id=1)
        response = self.client.get(reverse('blogger-detail', kwargs={'pk':blogger.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        blogger = Blogger.objects.get(id=1)
        response = self.client.get(reverse('blogger-detail', kwargs={'pk':blogger.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogger_detail.html')

class CommentsByUserListViewTest(TestCase):
    def setUp(self):
         # Create two users
        test_author1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_author2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_author1.save()
        test_author2.save()

        today = datetime.date.today()
        blogger = Blogger.objects.create(author=test_author1, bio='John Davison Rockefeller Sr. was an American business magnate and philanthropist. He is widely considered the wealthiest American of all time and the richest person in modern history. ')
        blog = Blog.objects.create(name='Why Africa is rich in minerals but its people are the poorest?', blogger=blogger, description='The great reason and cause for that is poor education system, which cause the people to lack awareness of their values in this planent and the whole universe at large', post_date=today)

        # Create a comment
        test_comment = Comment.objects.create(description='Yaah that is true, but also africans are so lazzy people to think about their future', blog=blog, author=test_author1, post_date=today)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-comments'))
        self.assertRedirects(response, '/accounts/login/?next=/blog/comments/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-comments'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'blog/comment_list_by_user.html')

class CommentCreateViewTest(TestCase):
    def setUp(self):
         # Create two users
        test_author1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_author2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_author1.save()
        test_author2.save()

        today = datetime.date.today()
        blogger = Blogger.objects.create(author=test_author1, bio='John Davison Rockefeller Sr. was an American business magnate and philanthropist. He is widely considered the wealthiest American of all time and the richest person in modern history. ')
        blog = Blog.objects.create(name='Why Africa is rich in minerals but its people are the poorest?', blogger=blogger, description='The great reason and cause for that is poor education system, which cause the people to lack awareness of their values in this planent and the whole universe at large', post_date=today)

        # Create a comment
        Comment.objects.create(description='Yaah that is true, but also africans are so lazzy people to think about their future', blog=blog, author=test_author1, post_date=today)

    def test_redirect_if_not_logged_in(self):
        comment = Comment.objects.get(id=1)
        response = self.client.get(reverse('comment-create', kwargs={'pk':comment.id}) )
        self.assertRedirects(response, '/accounts/login/?next=/blog/blog/1/comment/')

    def test_logged_in_uses_correct_template(self):
        comment = Comment.objects.get(id=1)
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('comment-create', kwargs={'pk':comment.id}) )

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'blog/comment_form.html')




    


