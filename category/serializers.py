from rest_framework import serializers
from .models import Category1, Category2, Category3


class Category3Serializers(serializers.ModelSerializer):
    class Meta:
        model = Category3
        fields = ['id', 'label', 'image', 'icon']


class Category2Serializers(serializers.ModelSerializer):
    children = Category3Serializers(many=True, read_only=True)

    class Meta:
        model = Category2
        fields = ['id', 'label', 'image', 'icon', 'children']


class Category1Serializers(serializers.ModelSerializer):
    children = Category2Serializers(many=True, read_only=True)

    class Meta:
        model = Category1
        fields = ['id', 'label', 'image', 'icon', 'children']
