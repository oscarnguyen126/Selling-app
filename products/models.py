from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='products')
    
    def __str__(self):
        return self.name

