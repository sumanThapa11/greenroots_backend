from asyncore import write
from statistics import mode
from django.forms import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from plants.models import CartItem, Category, CustomUser, Plants, Cart


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = CustomUser
        fields = ('email','password','password2','first_name','last_name','address','phone')
        extra_kwargs = {
            'first_name':{'required':True},
            'last_name':{'required':True},
            'address':{'required':True},
            'phone':{'required':True}
        }

    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields did not match."})

        return attrs

    def create(self,validated_data):
        user = CustomUser.objects.create_user(validated_data['email'],validated_data['first_name'],
        validated_data['last_name'],validated_data['address'],validated_data['phone'],validated_data['password'])

        user.save()

        return user





class PlantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plants
        fields = ['id','name','unit_price','suitable_temperature','description','image','category']


class CategorySerializer(serializers.ModelSerializer):
   
    plants = PlantSerializer(many=True,read_only = True)

    class Meta:
        model = Category
        fields = ['id','name','image','description','numberOfPlants','plants']

    

#for currently logged in user
class UserCartItemSerializer(serializers.ModelSerializer):
    
    plant = serializers.StringRelatedField()
    class Meta:
        model = CartItem
        fields = ['id','quantity','cart','plant','total']
        extra_kwargs = {"cart":{"required":False, "allow_null":True}}


#for currently logged in user
class UserCartSerializer(serializers.ModelSerializer):

    cart_item = UserCartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id','user','total','cart_item']
        extra_kwargs = {"user":{"required":False, "allow_null":True}}


class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['id','quantity','cart','plant','total']
        extra_kwargs = {"cart":{"required":False, "allow_null":True}}


class CartSerializer(serializers.ModelSerializer):

    cart_item = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id','user','total','cart_item']
        extra_kwargs = {"user":{"required":False, "allow_null":True}}

    def create(self, validated_data):
    
        return super().create(validated_data)


#to get all the plants in each category
# class PlantsInCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id',]

