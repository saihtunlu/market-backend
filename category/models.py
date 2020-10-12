from django.db import models


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category1(TrackableDateModel):
    label = models.TextField(max_length=2000, null=True)
    image = models.ImageField(
        upload_to='categories/category1/', null=True)
    icon = models.TextField(max_length=2000, null=True)
    slug = models.SlugField(unique=True, null=False)


class Category2(TrackableDateModel):
    main_category = models.ForeignKey(Category1, related_name='children',
                                      null=True, blank=True, on_delete=models.CASCADE)
    label = models.TextField(max_length=2000, null=True)
    image = models.ImageField(
        upload_to='categories/category2/', null=True)
    icon = models.TextField(max_length=2000, null=True)
    slug = models.SlugField(unique=True, null=False)


class Category3(TrackableDateModel):
    main_category = models.ForeignKey(Category2, related_name='children',
                                      null=True, blank=True, on_delete=models.CASCADE)
    label = models.TextField(max_length=2000, null=True)
    image = models.ImageField(
        upload_to='categories/category3/', null=True)
    icon = models.TextField(max_length=2000, null=True)
    slug = models.SlugField(unique=True, null=False)
