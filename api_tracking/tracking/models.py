from django.db import models
import uuid

class TrackingNumber(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    tracking_number = models.CharField(max_length=16, unique=True)
    origin_country_id = models.CharField(max_length=2)
    destination_country_id = models.CharField(max_length=2)
    weight = models.DecimalField(max_digits=5, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_id = models.UUIDField()
    customer_name = models.CharField(max_length=255)
    customer_slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.tracking_number