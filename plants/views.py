from ast import Is
from multiprocessing import context
from os import stat
from re import template
from signal import raise_signal
from django.http import response
from django.shortcuts import get_object_or_404, render

from django.db.models import Sum
from django.views.generic import TemplateView

from django.core.mail import send_mail

import requests
import json
import base64

from rest_framework import permissions

import pyotp

from PIL import Image
from urllib.request import urlopen

# from firebase_admin.messaging import Message, Notification
# from fcm_django.models import FCMDevice

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser

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
            category = get_object_or_404(Category,pk=pk)
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
    # permission_classes = [IsAuthenticated]

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

        url = "https://fcm.googleapis.com/fcm/send"

        registration_ids = []
        userDevices =  UserDeviceToken.objects.all()

        for device in userDevices:
            registration_ids.append(device.token)

        payload = json.dumps({
        "registration_ids": registration_ids,
        "notification": {
            "body": "Checkout our new plant.",
            "title": "New Plant!!",
            "android_channel_id": "greenroots",
            "sound": "false"
        }
        })

        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=AAAA454cXsk:APA91bGgCS-E896n4AiDFEs5vVA19vsqHgIoqp_fSa8AyZfyhiWW_osXBqnz8nPW8D-6Jt3_amXSHgDdTlumTHwKgp9PMrCoJGeMZNX39WfxNg8JeWXgAnFfTRRdpJKOCDAuBIzO4V-d'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
    
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
        # current_user = self.request.user
        # print(current_user.orders.all())
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

    def put(self,request,pk=None):
        payment = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payment, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self,request,pk):
        payment = get_object_or_404(Payment,pk=pk)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        plant_name = response["suggestions"][0]["plant_name"]
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

        no_plant_details = {"id":0,"name":plant_name}
        print(no_plant_details)
        return Response(no_plant_details,status=status.HTTP_202_ACCEPTED)


class UserDeviceTokenList(APIView):

    permission_classes=[IsAuthenticated]
    def get(self,request):
        device_tokens = UserDeviceToken.objects.all()
        serializer = UserDeviceTokenSerializer(device_tokens,many=True)
        return Response(serializer.data)

    def post(self,request):
       
        serializer = UserDeviceTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            UserDeviceToken.objects.get(token=serializer.validated_data['token']) 
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except UserDeviceToken.DoesNotExist:
            serializer.save(user_id=self.request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def delete(self,request,pk):
        device_token = get_object_or_404(UserDeviceToken,pk=pk)
        device_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendEmailToken(APIView):
    def post(self,request):
        serializer = SendEmailTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recepeint_email = serializer.validated_data['email']

        totp = pyotp.TOTP('base32secret3232')
        otp = str(totp.now())[:4]

        send_mail( "OTP for your login",
            otp,
            "st58470414826@gmail.com",
            [recepeint_email])
        return Response({'otp':otp},status=status.HTTP_200_OK)


# for chart
class TopPlants(TemplateView):
    
    template_name = 'plants/chart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        plants = PlantOrder.objects.values('plant').annotate(total_plants_sold=Sum('quantity')).order_by('-total_plants_sold')[:5]
        # print(plants)
        for plant in plants:
            single_plant = Plants.objects.get(id=plant['plant'])
            plant['plant'] = single_plant.name
            # print(single_plant.name)
       
        context["qs"] = plants
       
        return context
