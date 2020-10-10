from .models import Shop, ShopUser
from account.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from rest_framework import generics, pagination
from rest_framework.response import Response
from .serializers import ShopSerializers, ShopUserSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

# Create your views here.


class Shops(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Shop.objects.order_by('created_at').reverse()
    serializer_class = ShopSerializers
    pagination_class = pagination.PageNumberPagination


class SingleShop(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        shop_serializer = ShopSerializers(data=data)
        if shop_serializer.is_valid():
            shop_serializer.save()
            return Response(shop_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        slug = kwargs['slug']
        shop = Shop.objects.get(slug=slug)
        shop_serializer = ShopSerializers(shop, data=data)
        if shop_serializer.is_valid():
            shop_serializer.save()
            return Response(shop_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        shop = get_object_or_404(
            Shop, slug=slug)
        shop_serializer = ShopSerializers(shop, many=False)
        return Response(shop_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        slug = kwargs['slug']
        shop = Shop.objects.get(slug=slug)
        shop.delete()
        return Response('Success', status=status.HTTP_201_CREATED)


class ShopUsers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ShopUser.objects.order_by('created_at').reverse()
    serializer_class = ShopUserSerializers
    pagination_class = pagination.PageNumberPagination


class SingleShopUser(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        shop = Shop.objects.get(id=request.data['shop_id'])
        user = User.objects.get(id=request.data['user_id'])
        shopUser = ShopUser(user=user,
                            shop=shop)  # add foreign key
        shopUser_serializer = ShopUserSerializers(shopUser, data=data)
        if shopUser_serializer.is_valid():
            shopUser_serializer.save()
            return Response(shopUser_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(shopUser_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        shop = Shop.objects.get(id=request.data['shop_id'])
        shopUser = ShopUser.objects.get(id=request.data['id'])
        shopUser.shop = shop
        shopUser_serializer = ShopUserSerializers(shopUser, data=data)
        if shopUser_serializer.is_valid():
            shopUser_serializer.save()
            return Response(shopUser_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(shopUser_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        shopUser = get_object_or_404(
            ShopUser, id=id)
        shopUser_serializer = ShopUserSerializers(shopUser, many=False)
        return Response(shopUser_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        id = kwargs['id']
        shopUser = get_object_or_404(
            ShopUser, id=id)
        shopUser.delete()
        return Response('Success', status=status.HTTP_201_CREATED)
