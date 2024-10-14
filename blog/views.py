from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render

# Create your views here.
from . models import *
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .forms import CreateCommentForm
import random
from . forms import *
from django.urls import reverse

class ShowAllView(ListView):
    '''A view to show all Articles'''

    model = Article
    template_name = "blog/show_alls.html"
    context_object_name = 'articles'

class RandomArticleView(DetailView):
    # show one article selected at random

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" #note the singular name

    def get_object(self):
    # return the instance of the article object to show

        # get all articles
        all_articles = Article.objects.all() #SELECT *
        # pick one at random
        return random.choice(all_articles)
    
class ArticleView(DetailView):
    # show one article by its primary key

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" #note the singular name


class CreateCommentView(CreateView):
    '''on Get: sends back the form
    on Post: read the form data, create an instance of comment; save to database'''
    
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    # what to do after send
    def get_success_url(self) -> str:
        '''return the URL to redirect to after sucessful create'''
        # return "/blog/show_all"
        return reverse("article", kwargs=self.kwargs)
    
    def form_valid(self, form):
        '''this method executes after form submission'''
        print(f'CreateCommentView.form_valid(): form = {form.cleaned_data}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')

        #find the article with the PK from the url
        article = Article.objects.get(pk=self.kwargs['pk'])

        #attach the article to the new Comment
        # (forms.instance is the new comment objects)
        form.instance.article = article


        # delegate work to the superclass version of this method
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''build the template context data -
        a dict of key-value pair'''

        #get the super class version of context data
        context = super().get_context_data(**kwargs)

        #add the article to the context data
        article = Article.objects.get(pk=self.kwargs['pk'])

        context['article']= article
        return context