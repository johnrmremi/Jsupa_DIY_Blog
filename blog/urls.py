from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.PostListView.as_view(), name='blogs'),
    path('blog/<int:pk>', views.PostDetailView.as_view(), name='blog-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('comments/', views.CommentsByUserListView.as_view(), name='my-comments'),
    path('myblogs/', views.BlogsByBloggerListView.as_view(), name='my-blogs'),
    path('blog/<int:pk>/comment/', views.CommentCreate.as_view(), name='blog_comment'),
    path('comment/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment-delete'),
    path('blog/create/', views.PostCreate.as_view(), name='blog-create'),
    path('blog/<int:pk>/update', views.PostUpdate.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete', views.PostDelete.as_view(), name='blog-delete'),


]
