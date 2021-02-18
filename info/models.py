from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    # Для создания последовательностей из статей
    priority = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('priority',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_view', args=[self.id])
