from ast import Is
from os import stat
from django.http import response
from django.shortcuts import get_object_or_404, render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny

from plants.serializers import *
from plants.models import *


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    serializer_class = RegisterUserSerializer

    def post(self,request,format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user':serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryList(APIView):

    def get(self,request,pk=None):

        if pk is not None:
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(category)
           
            return Response(serializer.data)
        
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = CategorySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self,request,pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self,request,pk):
        category = get_object_or_404(Category,pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlantList(APIView):

    def get(self,request,pk=None):

        if pk is not None:
            plant = Plants.objects.get(id=pk)
            serializer = PlantSerializer(plant)
           
            return Response(serializer.data)
        
        plants = Plants.objects.all()
        serializer = PlantSerializer(plants,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PlantSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self,request,pk=None):
        plant = get_object_or_404(Plants, pk=pk)
        serializer = PlantSerializer(plant, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self,request,pk):
        plant = get_object_or_404(Plants,pk=pk)
        plant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartList(APIView):
    def get(self,request,pk=None):

        if pk is not None:
            cart = Cart.objects.get(id=pk)
            serializer = CartSerializer(cart)
           
            return Response(serializer.data)
        
        carts = Cart.objects.all()
        serializer = CartSerializer(carts,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = CartSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self,request,pk):
        cart = get_object_or_404(Cart,pk=pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartItemList(APIView):
    def get(self,request,pk=None):

        if pk is not None:
            cart_item = CartItem.objects.get(id=pk)
            serializer = CartItemSerializer(cart_item)
           
            return Response(serializer.data)
        
        cart_items = CartItem.objects.all()
        serializer = CartItemSerializer(cart_items,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = CartItemSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self,request,pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        serializer = CartItemSerializer(cart_item, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self,request,pk):
        cart_item = get_object_or_404(CartItem,pk=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)