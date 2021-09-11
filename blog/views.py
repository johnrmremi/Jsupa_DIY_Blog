from django.db.models.fields import DateField
from django.http import request
from django.shortcuts import render, get_object_or_404
import datetime

# Create your views here.

from .models import Blog, Blogger, Comment
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_blogs = Blog.objects.all().count()
    num_comments = Comment.objects.all().count()

    # The 'all()' is implied by default.
    num_bloggers = Blogger.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_blogs': num_blogs,
        'num_comments': num_comments,
        'num_bloggers': num_bloggers,
        'num_visits': num_visits,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5

class BlogDetailView(generic.DetailView):
    model = Blog

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
    permission_required = 'blog.can_add_and_update_and_delete_blog'
    model = Blog
    template_name ='blog/blog_list_by_blogger.html'
    paginate_by = 5 

    def get_queryset(self):
        return Blog.objects.filter(blogger__author = self.request.user)

class CommentCreate(LoginRequiredMixin, CreateView):
    """ Form for adding a blog comment. Requires login. """
    model = Comment
    fields = ['description']

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(CommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        # context['blog'] = 'get_object_or'
        context['blog'] = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.blog=get_object_or_404(Blog, pk = self.kwargs['pk'])

        # Adding date of posting to be this time
        form.instance.post_date = datetime.datetime.now()
        # Call super-class form validation behavior
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self): 
        """
        After posting comment return to associated blog.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],})

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['description']
    template_name ='blog/comment_update.html'

    def form_valid(self, form):

        # Updating date of posting to be this time
        form.instance.post_date = datetime.datetime.now()
        # Call super-class form validation behavior
        return super(CommentUpdate, self).form_valid(form)
    
    success_url = reverse_lazy('my-comments')

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('my-comments')


class BlogCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'blog.can_add_and_update_and_delete_blog'
    model = Blog
    fields = ['name', 'description']
    
    def form_valid(self, form):
        """
        Add blogger and associated data to form data before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as blogger of blog

        form.instance.blogger=get_object_or_404(Blogger, author = self.request.user)

        # Adding date of posting to be this time
        form.instance.post_date = datetime.datetime.now()
        # Call super-class form validation behavior
        return super(BlogCreate, self).form_valid(form)

    success_url = reverse_lazy('my-blogs')

class BlogUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'blog.can_add_and_update_and_delete_blog'
    model = Blog
    fields = ['name', 'description'] 

    def form_valid(self, form):

        form.instance.blogger=get_object_or_404(Blogger, author = self.request.user)

        # Adding date of posting to be this time
        form.instance.post_date = datetime.datetime.now()
        # Call super-class form validation behavior
        return super(BlogUpdate, self).form_valid(form)

    success_url = reverse_lazy('my-blogs')

class BlogDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'blog.can_add_and_update_and_delete_blog'
    model = Blog
    success_url = reverse_lazy('my-blogs')

    

   

    


    



































        