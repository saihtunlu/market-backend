from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Shop, ShopUser


class GetUserSerializers(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = ShopUser
        fields = ['user', 'id']


class ShopSerializers(serializers.ModelSerializer):
    users = GetUserSerializers(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ['id', 'cover', 'logo', 'name',
                  'address', 'phone', 'slug', 'created_at', 'users', ]


class ShopUserSerializers(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    shop = ShopSerializers(many=False, read_only=True)

    class Meta:
        model = ShopUser
        fields = ['user', 'id', 'shop']
