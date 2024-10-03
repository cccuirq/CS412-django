#blog/models.py
#define data models(objects) for use in the blog application
#when modify data attributes run make migration
from django.db import models

# Create your models here.
class Article(models.Model):
    '''Encapsulate the data for a blog Article by some author'''

    #data attributes:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)#new field

    def __str__(self):
        '''Return a string representation of this Article.'''
        return f'{self.title} by {self.author}'