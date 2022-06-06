from email.policy import default
from itertools import product
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.base import Model
from django.db.models.signals import post_save
import json
from django.forms import ValidationError
import requests
import re


class CustomUserManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,address,phone,password=None):

        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not address:
            raise ValueError('Users must have an address')
        if not phone:
            raise ValueError('Usersmust have a phone number')

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            address = address,
            phone = phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,email,first_name,last_name,address,phone,password=None): 
        user = self.create_user(
            email,
            password=password,
            first_name = first_name,
            last_name = last_name,
            address = address,
            phone = phone,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=70,unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','address','phone']

    objects = CustomUserManager()    

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Category(models.Model):

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100)
    image = models.ImageField(default='plant1.PNG')
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    @property
    def numberOfPlants(self):
        return self.plants.all().count


class Payment(models.Model):
    payment_type = models.CharField(max_length=100)

    def __str__(self):
        return self.payment_type

def validate_suitable_temperature(value):
    pattern = '[0-9][0-9]-[0-9][0-9]'
    result = re.match(pattern,value)

    if result == None:
        raise ValidationError('Please enter a valid temperatue eg: 02-27')

class Plants(models.Model):

    class Meta:
        verbose_name_plural = "plants"

    name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)
    suitable_temperature = models.CharField(validators=[validate_suitable_temperature], max_length=5)
    description  = models.TextField()
    image = models.ImageField(default='indoor.jpg')
    category = models.ForeignKey(Category, related_name='plants', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cart(models.Model):
    # total = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.OneToOneField(CustomUser,related_name='cart', on_delete=models.CASCADE)

    def __str__(self):
        return "cart of " + str(self.user)

    @property 
    def total(self):
        amount = 0
        for item in self.cart_item.all():
            amount += item.total
        return round(amount,2)


class CartItem(models.Model):
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, related_name='cart_item', on_delete=models.CASCADE)
    plant = models.ForeignKey(Plants, related_name='plant', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.plant)

    @property
    def total(self):
        return (self.quantity * self.plant.unit_price)

    @property
    def plantId(self):
        return (self.plant.id)

class Orders(models.Model):

    class Meta:
        verbose_name_plural = "Orders"

    date = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, related_name='orders', on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=200)

    def __str__(self):
        return "order of "+ str(self.user)


class PlantOrder(models.Model):
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=8, decimal_places=2)
    order = models.ForeignKey(Orders, related_name='plant_order', on_delete=models.CASCADE)
    plant = models.ForeignKey(Plants, related_name='plant_order',on_delete=models.CASCADE)

    def __str__(self):
        return str(self.plant)


class UserPlant(models.Model):
    user_id = models.ForeignKey(CustomUser,related_name='users_plant',on_delete=models.CASCADE)
    plant_id = models.ForeignKey(Plants,related_name='users_plant',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id','plant_id')


class UserDeviceToken(models.Model):
    user_id = models.ForeignKey(CustomUser,related_name='user_device_token',on_delete=models.CASCADE)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def send_notification(sender, instance, created, **kwargs):

    if created:
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
        print("notification sent")
    
post_save.connect(send_notification, sender=Plants)