from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Shop(TrackableDateModel):
    name = models.TextField(max_length=2000, null=True)
    cover = models.ImageField(
        upload_to='shops/', null=True)
    logo = models.ImageField(
        upload_to='shops/', null=True)
    phone = models.TextField(max_length=2000, null=True)
    address = models.TextField(max_length=2000, null=True)
    slug = models.SlugField(unique=True, null=False)


class ShopUser(TrackableDateModel):
    user = models.OneToOneField(User, related_name='shop',
                                null=True, blank=True, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='users',
                             null=True, blank=True, on_delete=models.CASCADE)
