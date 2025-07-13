"""Models for the blog application.

Defines Post and Comment models for blog content and discussion.
"""

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from users.models import CustomUser

class PublishedManager(models.Manager):
    """Manager to return only published posts."""

    def get_queryset(self):
        """Return queryset of published posts only."""
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class DraftManager(models.Manager):
    """Manager to return only draft posts."""

    def get_queryset(self):
        """Return queryset of draft posts only."""
        return super().get_queryset().filter(status=Post.Status.DRAFT)

class Post(models.Model):
    """A blog post with title, content, author, status, tags, and image.

    Attributes:
      title: The title of the blog post.
      slug: URL-friendly unique identifier for the post.
      content: The main content of the post.
      publish: The datetime when the post was published.
      created_at: The datetime when the post was created.
      updated_at: The datetime when the post was last updated.
      author: The user who wrote the post.
      status: The publication status (draft or published).
      tags: Tags associated with the post.
      users_like: Users who liked the post.
      post_image: The main image for the post.
    """

    class Status(models.TextChoices):
        """Publication status choices for posts."""
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, null=False, unique=True)
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    objects = models.Manager()
    published = PublishedManager()
    draft = DraftManager()
    tags = TaggableManager()
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='post_liked',
        blank=True
    )
    post_image = models.ImageField(upload_to='post_pics')

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        """Return the post title."""
        return str(self.title)

    def get_absolute_url(self):
        """Return the URL to the post detail page."""
        return reverse('blog:post-detail', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        """Save the post, generating a slug if needed.

        Args:
          *args: Variable length argument list.
          **kwargs: Arbitrary keyword arguments.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Comment(models.Model):
    """A comment on a blog post.

    Attributes:
      post: The blog post this comment is attached to.
      name: The name of the comment author.
      email: The email of the comment author.
      body: The comment text.
      created: The datetime when the comment was created.
      updated: The datetime when the comment was last updated.
      active: Whether the comment is visible.
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        """Return a string representation of the comment."""
        return f'Comment by {self.name} on {self.post}'
