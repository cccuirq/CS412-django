#blog/models.py
#define data models(objects) for use in the blog application
#when modify data attributes run make migration
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    '''Encapsulate the data for a blog Article by some author'''
    #each Article will associated with a User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #data attributes:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True)#new field
    image_file = models.ImageField(blank=True) # an actual image

    def __str__(self):
        '''Return a string representation of this Article.'''
        return f'{self.title} by {self.author}'
    
    def get_comments(self):
        '''retrieve all comments for this Article.'''

        # use the ORM to filter Comments where this instance of article is ths PK
        comments = Comment.objects.filter(article=self)
        return comments
    
    def get_absolute_url(self):
        return reverse('article', kwargs={'pk':self.pk})
    
class Comment(models.Model):
    # encapsulate a comment on an article

    # create a 1 to many relationship between Articles and Comments
    article = models.ForeignKey("Article", on_delete=models.CASCADE) ### IMPORTANT
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this object.'''
        return f'{self.text}'
