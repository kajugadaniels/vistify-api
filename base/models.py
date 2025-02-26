import os
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField

def category_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    return f'categories/category_{slugify(instance.name)}_{timestamp}{file_extension}'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    image = ProcessedImageField(
        upload_to=category_image_path,
        processors=[ResizeToFill(800, 800)],
        options={'quality': 90},
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _generate_unique_slug(self):
        """Generate a unique slug"""
        base_slug = slugify(self.name)
        slug = f"{base_slug}"
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}"
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else "Unnamed Category"

    class Meta:
        verbose_name_plural = "Categories"