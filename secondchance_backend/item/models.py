import uuid
from django.conf import settings
from django.db import models
from useraccount.models import User


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    rental_price = models.FloatField()
    quantity = models.IntegerField()
    condition = models.CharField(max_length=100)
    category = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    favorited = models.ManyToManyField(User, related_name="favorites", blank=True)
    image = models.ImageField(
        upload_to="uploads/items"
    )
    seller = models.ForeignKey(
        User, related_name="items", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return f"{settings.WEBSITE_URL}{self.image.url}"

    @property
    def location(self):
        return f"{self.country}"

    class Meta:
        verbose_name_plural = "Items"


class Rental(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(
        Item, related_name="rentals", on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_days = (
        models.IntegerField()
    )
    quantity = models.IntegerField()
    total_price = models.FloatField()
    created_by = models.ForeignKey(
        User, related_name="rentals", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Rentals"