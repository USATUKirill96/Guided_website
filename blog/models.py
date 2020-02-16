from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class PublishedManager(models.Manager):
    """Собственный менеджер модели. По сути, не обязателен,
    функционал сводится к автоматической фильтрации статей по параметру опубликованной.
    Командой Post.published() будет выводить все опубликованные статьи"""
    def get_queryset(self):
        return super().get_queryset().filter(status='published')



class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=
                              STATUS_CHOICES, default='draft')
    objects = models.Manager() #Здесь менеджер по умолчанию
    published = PublishedManager() #А здесь кастомный, который выводит только опубликованные

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                        self.publish.month, self.publish.day, self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Класс комментария. Привязывается по внешнему ключу к конкретному посту
    Атрибут related_name позволяет получить доступ
    к комментариям конкретной статьи. Теперь мы сможем обращаться к статье
    из комментария, используя запись comment.post, и к комментариям статьи при
    помощи post.comments.all()."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
