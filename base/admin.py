from base.models import *
from django.contrib import admin

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
# Place Admin
# -------------------
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'province', 'district', 'views', 'created_at')
    search_fields = ('name', 'category__name', 'province', 'district')
    list_filter = ('category', 'province', 'district', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tags',)  # Allows selecting multiple tags in a better UI

# -------------------
# Place Image Admin
# -------------------
@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'place', 'caption', 'created_at')
    search_fields = ('place__name', 'caption')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """Display a thumbnail preview of the image in the admin panel."""
        return obj.image_preview() if obj.image else "No Image"

    image_preview.short_description = "Image Preview"

# -------------------
# Place Social Media Admin
# -------------------
@admin.register(PlaceSocialMedia)
class PlaceSocialMediaAdmin(admin.ModelAdmin):
    list_display = ('place', 'phone_number', 'email', 'instagram', 'twitter', 'facebook')
    search_fields = ('place__name', 'phone_number', 'email', 'instagram', 'twitter', 'facebook')
    list_filter = ('place',)

