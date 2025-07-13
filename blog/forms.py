"""Forms for the blog application.

Defines forms for comments and search functionality.
"""

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """Form for submitting a comment on a blog post.

    Attributes:
      Meta: Model and fields for the form.
    """
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class SearchForm(forms.Form):
    """Form for searching blog posts by query string.

    Attributes:
      query: The search query string.
    """
    query = forms.CharField()
