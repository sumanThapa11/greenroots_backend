from ast import Is
from os import stat
from signal import raise_signal
from django.http import response
from django.shortcuts import get_object_or_404, render

import requests
import base64

from PIL import Image
from urllib.request import urlopen


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
        
    def patch(self,request,pk):
        plant = get_object_or_404(Plants,pk=pk)
        serializer = PlantSerializer(plant,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'partial data updated'})

    def delete(self,request,pk):
        plant = get_object_or_404(Plants,pk=pk)
        plant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#for getting the cart of currently logged in user
class UsersCart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        cart = get_object_or_404(Cart,user=self.request.user)
        serializer = UserCartSerializer(cart)
        if(len(serializer.data["cart_item"])!=0):
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_202_ACCEPTED)
    
    def delete(self,request):
        cart = get_object_or_404(Cart,pk=self.request.user.cart.id)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartList(APIView):

    permission_classes = [IsAuthenticated]
    
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
        try:
            cart = self.request.user.cart.id
            return Response({'message':'Cart already exists'},status=status.HTTP_201_CREATED)
        except:
            serializer.save(user=self.request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        # serializer.save(user=self.request.user)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
       
    
    def delete(self,request,pk):
        cart = get_object_or_404(Cart,pk=pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartItemList(APIView):

    permission_classes = [IsAuthenticated]
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

        try:
            cartItem = CartItem.objects.get(plant=serializer.validated_data['plant'],cart=self.request.user.cart)
            print(cartItem)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            serializer.save(cart=self.request.user.cart)
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


class OrderList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        orders = Orders.objects.all()
        serializer = OrderSerializer(orders,many=True)
        current_user = self.request.user
        print(current_user.orders.all())
        return Response(serializer.data)

    def post(self,request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def delete(self,request,pk):
        order = get_object_or_404(Orders,pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlantOrderList(APIView):
    def get(self,request):
        plantOrder = PlantOrder.objects.all()
        serializer = PlantOrderSerializer(plantOrder,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PlantOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class PaymentList(APIView):

    def get(self,request):
        payment = Payment.objects.all()
        serializer = PaymentSerializer(payment,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class UsersPlantList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        users_plant = UserPlant.objects.filter(user_id=self.request.user.id)
        serializer = UsersPlantSerializer(users_plant,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = UsersPlantSerializer(data=request.data)
        users_plants = UserPlant.objects.filter(user_id=self.request.user.id)
        serializer.is_valid(raise_exception=True)

        for users_plant in users_plants:
            if (serializer.validated_data['plant_id'] == users_plant.plant_id):
                return Response('plant already exists',status=status.HTTP_201_CREATED)

        serializer.save(user_id=self.request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class UsersPlantDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        plant_ids = []
        users_plants = UserPlant.objects.filter(user_id=self.request.user.id)
        for users_plant in users_plants:
            plant_ids.append(users_plant.plant_id)
        users_plants_details = Plants.objects.filter(name__in=plant_ids) 
        serializer = PlantSerializer(users_plants_details,many=True)
        return Response(serializer.data)


class PlantScanner(APIView):

    def get(self,request):
        plants = Plants.objects.all()
        for plant in plants:
            print (plant.name)
        return Response(status=status.HTTP_200_OK)

    def post(self,request):
        serializer = PlantScannerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(serializer.validated_data['base64Image'])

        api_key = '53HrxyOMU2WVk5Qd1QTDYzAjOTabAJwj6iqjgfvZIzuBJ8yfZm'

        # with open("", "rb") as file:
        #     images = [base64.b64encode(file.read()).decode("ascii")]

        images = [serializer.validated_data['base64Image']]

        json_data = {
            "images": images,
            "modifiers": ["crops_fast"],
            "plant_details": ["common_names","name_authority","synonyms"]
        }

        response = requests.post(
            "https://api.plant.id/v2/identify",
            json=json_data,
            headers={
                "Content-Type": "application/json",
                "Api-Key": api_key
            }).json()
        
        print(response["suggestions"][0]["plant_name"].lower())    
        print(response["suggestions"][0]["plant_details"]["scientific_name"])
        print(response["suggestions"][0]["plant_details"]["common_names"])

        plants = Plants.objects.all()
        for plant in plants:
            if (plant.name.lower()) == (response["suggestions"][0]["plant_name"].lower()) or (plant.name.lower()) == (response["suggestions"][0]["plant_details"]["scientific_name"].lower()):
                print(plant.name)
                plant_details = {"id":plant.id,"name":plant.name}
                return Response(plant_details,status=status.HTTP_200_OK)
            
            for commonName in response["suggestions"][0]["plant_details"]["common_names"]:
                if (plant.name.lower()) == (commonName.lower()):
                    plant_details = {"id":plant.id,"name":plant.name}
                    return Response(plant_details,status=status.HTTP_200_OK)
        
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)