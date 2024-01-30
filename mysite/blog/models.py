from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices): #подкласс enum для отслеживания статутса поста
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish') # поле уникально для даты публикации
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True) #записывается время, при создании объекта (при создании поста в БД)
    updated = models.DateTimeField(auto_now=True) #обновляет дату и время каждый раз при изменении (сохранении) объекта (поста) в БД
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager() # менеджер, применяемый по умолчанию
    published = PublishedManager() # конкретно-прикладной менеджер для извлечения опубликованных постов
    tags = TaggableManager() # менеджер тегов для добавления, извлечения и удаления тегов из объекта Post

    class Meta:
        ordering = ['-publish'] #Сортировка результатов по полю publish в обратном порядке (от более новых к старым)
        indexes = [
            models.Index(fields=['-publish']) #создание индекса в БД по полю publish для более быстрого доступа к данным
        ]

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug]) # возвращение канонического url, обращение к url по имени благодаря reverse

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return f'Комментарий {self.name} на {self.post}'


