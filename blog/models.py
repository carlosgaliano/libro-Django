from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")
    
        
class DraftManager(models.Manager):
    def get_queryset(self):
        return models.Manager.get_queryset(self).filter(status="draft")
    

# clase Post
class Post(models.Model):
    STATUS_CHOICES = {
        ('draft', 'Draft'),
        ('published', 'Published'),
    }
    
    tittle = models.CharField(max_length=250, verbose_name="titulo")
    slug = models.SlugField(max_length=250, unique_for_date='publish', \
                            verbose_name="urlAbreviada")
    author = models.ForeignKey(User, on_delete=models.CASCADE, \
                               related_name='user_posts')
    body = models.TextField(verbose_name="")
    publish = models.DateTimeField(default=timezone.now, \
                                   verbose_name="publicar")
    created = models.DateTimeField(auto_now_add=True, verbose_name="creado")
    updated = models.DateTimeField(auto_now=True, verbose_name="actualizado")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, \
                              default='draft', verbose_name="estado")
    
    objects = models.Manager() # gestor por defecto
    published = PublishedManager() # nuevo gestor
    draft = DraftManager()
    
    
    class Meta:
        ordering = ('-publish',)
        
    def __str__(self):
        return self.tittle
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])