from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.PostListView.as_view(), name='blogs'),
    path('blog/<int:pk>', views.PostDetailView.as_view(), name='blog-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('mycomments/', views.CommentsByUserListView.as_view(), name='my-comments'),
    path('myblogs/', views.BlogsByBloggerListView.as_view(), name='my-blogs'),
]
