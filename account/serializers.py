from rest_framework.fields import ReadOnlyField
from .models import User
from shop.models import ShopUser
from rest_framework import serializers
# from permission.serializers import UserRoleSerializers


class UserSerializer(serializers.ModelSerializer):
    # role = UserRoleSerializers(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'first_name',
                  'last_name', 'email', 'avatar', 'username', 'shop', 'user_role']
