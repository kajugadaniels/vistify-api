from base.models import *
from django.contrib import admin
from django.utils.html import format_html

# -------------------
# Place Image Inline Admin
# -------------------
class PlaceImageInline(admin.TabularInline):  # or admin.StackedInline for vertical layout
    model = PlaceImage
    extra = 1  # Allows adding one extra blank image field
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        """Display a small preview of the uploaded image in the admin panel."""
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="border-radius:5px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = "Image Preview"

# -------------------
# Place Social Media Inline Admin
# -------------------
class PlaceSocialMediaInline(admin.StackedInline):
    model = PlaceSocialMedia
    extra = 1  # Only one social media entry per place
    max_num = 1  # Prevents multiple social media records per place

# -------------------
# Category Admin
# -------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('created_at', 'updated_at')

# -------------------
# Tag Admin
# -------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

# -------------------
# Place Admin (with inline images & social media)
# -------------------
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'province', 'district', 'views', 'created_at')
    search_fields = ('name', 'category__name', 'province', 'district')
    list_filter = ('category', 'province', 'district', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tags',)  # Allows selecting multiple tags in a better UI
    inlines = [PlaceImageInline, PlaceSocialMediaInline]  # Add images & social media directly

# -------------------
# Place Image Admin
# -------------------
@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'place', 'caption', 'created_at')
    search_fields = ('place__name', 'caption')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """Display a small thumbnail preview of the image in the admin panel."""
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="border-radius:5px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = "Image Preview"

# -------------------
# Place Social Media Admin
# -------------------
@admin.register(PlaceSocialMedia)
class PlaceSocialMediaAdmin(admin.ModelAdmin):
    list_display = ('place', 'phone_number', 'email', 'instagram', 'twitter', 'facebook')
    search_fields = ('place__name', 'phone_number', 'email', 'instagram', 'twitter', 'facebook')
    list_filter = ('place',)
