## blogs/urls.py
## description: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views

#create a list of URLs for this app:
urlpatterns = [
    # path(url, view, name)
    path(r'', views.RandomArticleView.as_view(), name = "random"),
    path(r'show_alls', views.ShowAllView.as_view(), name = "show_alls"),
    path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"),
    # path(r'create_comment', views.CreateCommentView.as_view(), name="create_comment"),
    path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name="create_comment"),
    path(r'create_article', views.CreateArticleView.as_view(), name='create_article'),
    path(r'article/<int:pk>/update', views.UpdateArticleView.as_view(), name="update_article"),
    path(r'delete_comment/<int:pk>', views.DeleteCommentView.as_view(), name='delete_comment'),
]