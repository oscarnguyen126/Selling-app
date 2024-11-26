from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Product
        fields = ['uuid', 'name', 'description', 'price', 'created_at', 'updated_at', 'owner',]
        