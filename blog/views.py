from django.shortcuts import render

# Create your views here.

from .models import Post, Blogger, Comment
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_posts = Post.objects.all().count()
    num_comments = Comment.objects.all().count()

    # The 'all()' is implied by default.
    num_bloggers = Blogger.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_posts': num_posts,
        'num_comments': num_comments,
        'num_bloggers': num_bloggers,
        'num_visits': num_visits,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class PostListView(generic.ListView):
    model = Post
    paginate_by = 5

class PostDetailView(generic.DetailView):
    model = Post

class BloggerListView(generic.ListView):
    model = Blogger

class BloggerDetailView(generic.DetailView):
    model = Blogger

class CommentsByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing comments for of current user."""
    model = Comment
    template_name ='blog/comment_list_by_user.html'
    paginate_by = 5

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

class BlogsByBloggerListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing bloggs for of current blogger."""
    permission_required = 'blog.can_view_blogs'
    model = Post
    template_name ='blog/blog_list_by_blogger.html'
    paginate_by = 5 

    def get_queryset(self):
        return Post.objects.all()