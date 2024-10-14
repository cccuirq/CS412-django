from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Comment
         # which fields from model should we use
        # fields = ['article', 'author', 'text', ]
        fields = ['author', 'text', ]