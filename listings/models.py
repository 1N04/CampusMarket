from django.db import models
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    icon = models.CharField(max_length=50, blank=True, help_text='Bootstrap icon class, e.g. bi-book')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('listings:category', kwargs={'slug': self.slug})


class Condition(models.TextChoices):
    BRAND_NEW = 'brand_new', 'Brand New'
    LIKE_NEW = 'like_new', 'Like New'
    GOOD = 'good', 'Good'
    FAIR = 'fair', 'Fair'
    PARTS_ONLY = 'parts_only', 'Parts Only'


class Item(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items', verbose_name='Category')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items', verbose_name='Seller')
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.GOOD, verbose_name='Condition')
    image = models.ImageField(upload_to='items/', blank=True, null=True, verbose_name='Image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True, verbose_name='Available')
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listings:item_detail', kwargs={'pk': self.pk})
