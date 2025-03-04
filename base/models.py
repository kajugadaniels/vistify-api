import os
import random
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import format_html
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.validators import RegexValidator, URLValidator, EmailValidator

def category_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    return f'categories/category_{slugify(instance.name)}_{timestamp}{file_extension}'

def place_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    place_slug = slugify(instance.caption if instance.caption else instance.place.name)
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    return f'places/place_{place_slug}_{timestamp}{file_extension}'

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

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def _generate_unique_slug(self):
        """Generate a unique slug"""
        base_slug = slugify(self.name)
        slug = base_slug
        while Tag.objects.filter(slug=slug).exists():
            slug = f"{base_slug}"
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tags"

class Place(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='places', null=True, blank=True)
    province = models.CharField(max_length=500, null=True, blank=True)
    district = models.CharField(max_length=500, null=True, blank=True)
    sector = models.CharField(max_length=500, null=True, blank=True)
    cell = models.CharField(max_length=500, null=True, blank=True)
    village = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.FloatField(validators=[RegexValidator(regex=r'^-?([1-8]?\d(\.\d+)?|90(\.0+)?)$', message='Enter a valid latitude (-90 to 90).')], null=True, blank=True)
    longitude = models.FloatField(validators=[RegexValidator(regex=r'^-?((1[0-7]\d)|(\d{1,2}))(\.\d+)?$', message='Enter a valid longitude (-180 to 180).')], null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def _generate_unique_slug(self):
        """Generate a unique slug"""
        base_slug = slugify(self.name)
        slug = base_slug
        while Place.objects.filter(slug=slug).exists():
            slug = f"{base_slug}"
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super(Place, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Places"

class PlaceImage(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="images")
    image = ProcessedImageField(
        upload_to=place_image_path,
        processors=[ResizeToFill(1080, 600)],
        options={'quality': 90},
        null=True,
        blank=True,
    )
    caption = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def image_preview(self):
        """Display a thumbnail of the place image in the list view."""
        if self.image:
            return format_html('<img src="{}" width="50" height="50" />', self.image.url)
        return "No image"
    image_preview.short_description = "Image Preview"

    def __str__(self):
        return f"{self.place.name} Image" if self.place else "Place Image"

class PlaceSocialMedia(models.Model):
    place = models.OneToOneField(
        'Place', 
        on_delete=models.CASCADE, 
        related_name='social_media'
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    tiktok = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    whatsapp = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Social Media for {self.place.name}" if self.place else "Place Social Media"

class PlaceMenu(models.Model):
    place = models.ForeignKey(
        'Place',
        on_delete=models.CASCADE,
        related_name='menu_items'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.place.name}"