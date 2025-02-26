import os
import random
from django.db import models
from account.managers import CustomUserManager
from django.utils import timezone
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission

def user_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'users/user_{slugify(instance.name)}_{instance.phone_number}_{instance.email}{file_extension}'

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(unique=True, max_length=255, null=True, blank=True)
    phone_number = models.CharField(unique=True, max_length=20, null=True, blank=True)
    image = ProcessedImageField(
        upload_to=user_image_path,
        processors=[ResizeToFill(1270, 1270)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True
    )
    password = models.CharField(max_length=255, null=True, blank=True)
    reset_otp = models.CharField(max_length=7, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    # Custom related names to prevent clashes with auth models
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='account_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, 
        related_name='account_user_permissions',
        blank=True
    )

    def generate_username(self):
        """Generate a unique username based on the name and a random 4-digit number."""
        base_username = slugify(self.name) if self.name else "user"
        random_digits = str(random.randint(1000, 9999))
        return f"{base_username}-{random_digits}"

    def save(self, *args, **kwargs):
        # Regenerate username if not set or if the name has changed
        if not self.username or (self.name and self.pk):
            self.username = self.generate_username()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
