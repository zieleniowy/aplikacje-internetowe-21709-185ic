from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User 
from django.urls import reverse
# from django.contrib.auth.models import AbstractUser

class PublishedManager(models.Manager): 
    def get_queryset(self): 
        return super(PublishedManager, self).get_queryset().filter(status='published')

class UserDescription(models.Model):
    user = models.ForeignKey(User, 
        on_delete=models.CASCADE,
        related_name='descriptions',
        null=False)
    photo = models.CharField(max_length=128, null=True)
    content = models.CharField(max_length=250)


class Post(models.Model): 
    STATUS_CHOICES = ( 
        ('draft', 'Draft'), 
        ('published', 'Published'), 
    ) 
    title = models.CharField(max_length=250) 
    slug = models.SlugField(max_length=250,  
                            unique_for_date='publish') 
    author = models.ForeignKey(User, 
                               on_delete=models.CASCADE,
                               related_name='blog_posts',
                               null=False) 
    authorDesc = models.ForeignKey(UserDescription, related_name='blog_posts', on_delete=models.CASCADE, null=False)
    body = models.TextField() 
    desc = models.TextField(default='')
    publish = models.DateTimeField(default=timezone.now) 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    status = models.CharField(max_length=10,  
                              choices=STATUS_CHOICES, 
                              default='draft') 
    
    objects = models.Manager() # The default manager. 
    published = PublishedManager() # Our custom manager.
    class Meta: 
        ordering = ('-publish',) 

    def __str__(self): 
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
