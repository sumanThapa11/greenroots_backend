from rest_framework.test import APITestCase

from plants.models import *

import json

from rest_framework import status

class CategoryCreateTestCase(APITestCase):
    def test_create_category(self):
        initial_category_count = Category.objects.count()
        category_attrs = {
            'name':'hanging',
            # 'image': "static/hanging.jpg",
            'description': 'can be decorated by hanging around the house'
        }

        response = self.client.post('/api/category/',category_attrs)
        if response.status_code != 201:
            print(response.data)
        for attr, expected_value in category_attrs.items():
            self.assertEqual(response.data[attr],expected_value)
        self.assertEqual(Category.objects.count(),initial_category_count + 1,)


class CategoryDestroyTestCase(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
             name= 'hanging',
            # 'image': "static/hanging.jpg",
            description = 'can be decorated by hanging around the house'
        )
        return super().setUp()

    def test_delete_category(self):
        initial_category_count = Category.objects.count()
        category_id = Category.objects.first().id
        self.client.delete('/api/category/{}/'.format(category_id))
        self.assertEqual(Category.objects.count(),initial_category_count - 1) 
        self.assertRaises(Category.DoesNotExist,Category.objects.get, id=category_id,)


class CategoryListTestCase(APITestCase):
    def test_list_categories(self):
        response = self.client.get('/api/category/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class CategoryUpdateTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name= 'hanging',
            # 'image': "static/hanging.jpg",
            description = 'can be decorated by hanging around the house'
        )
        return super().setUp()

    def test_update_category(self):
        category = Category.objects.first()
        response = self.client.put('/api/category/{}/'.format(category.id),
        {
            'name':'outdoor',
            'description':'can grow outside of the house',
        },
        format = 'json',
        )
        updated = Category.objects.get(id=category.id)
        self.assertEqual(updated.name,'outdoor')


class PlantCreateTestCase(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            id = 1,
            name= 'hanging',
            # 'image': "static/hanging.jpg",
            description = 'can be decorated by hanging around the house'
        )
        return super().setUp()

    def test_create_plant(self):
        initial_plant_count = Plants.objects.count()
        plant_attrs = {
            "name": "cactus",
            "unit_price": '12.00',
            "suitable_temperature":"12-35",
            "description": "grows in hot climate",
            "category": 1
        }
        
        response = self.client.post('/api/plants/',plant_attrs,format='json')
        if response.status_code != 201:
            print(response.data)
        for attr, expected_value in plant_attrs.items():
            self.assertEqual(response.data[attr],expected_value)
        self.assertEqual(Plants.objects.count(),initial_plant_count + 1,)
        
class PlantDestroyTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            id = 1,
            name= 'hanging',
            # 'image': "static/hanging.jpg",
            description = 'can be decorated by hanging around the house'
        )

        self.plant = Plants.objects.create(
            name = "cactus",
            unit_price = 12.0,
            suitable_temperature = "12-30",
            description = "grows in hot climate",
            category = self.category
        )
        return super().setUp()

    def test_delete_plant(self):
        initial_plant_count = Plants.objects.count()
        plant_id = Plants.objects.first().id
        self.client.delete('/api/plants/{}/'.format(plant_id))
        self.assertEqual(Plants.objects.count(),initial_plant_count - 1)
        self.assertRaises(Plants.DoesNotExist,Plants.objects.get, id = plant_id)


class PlantListTestCase(APITestCase):
    def test_list_plants(self):
        response = self.client.get('/api/plants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PlantUpdateTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            id = 1,
            name= 'hanging',
            # 'image': "static/hanging.jpg",
            description = 'can be decorated by hanging around the house'
        )
        self.plant = Plants.objects.create(
            name = "cactus",
            unit_price = 12.0,
            suitable_temperature = "12-30",
            description = "grows in hot climate",
            category = self.category
        )
        return super().setUp() 

    def test_update_plant(self):
        plant = Plants.objects.first()
        response = self.client.put('/api/plants/{}/'.format(plant.id),
        {
            "name": "triangle cactus",
            "unit_price": '12.00',
            "suitable_temperature":"12-35",
            "description": "grows in hot climate",
            "category": 1
        },
        format = 'json', )
        updated = Plants.objects.get(id=plant.id)
        self.assertEqual(updated.name,'triangle cactus')


class PaymentCreateTestCase(APITestCase):
    def test_create_payment(self):
        initial_payment_count = Payment.objects.count()
        payment_attrs = {
            'payment_type' : 'khalti',
        }

        response = self.client.post('/api/payments/',payment_attrs)
        if response.status_code != 201:
            print(response.data)
        for attr, expected_value in payment_attrs.items():
            self.assertEqual(response.data[attr],expected_value)
        self.assertEqual(Payment.objects.count(), initial_payment_count + 1)


class PaymentDestroyTestCase(APITestCase):
    def setUp(self):
        self.payment = Payment.objects.create(
            payment_type = 'khalti'
        )
        return super().setUp()

    def test_delete_payment(self):
        initial_payment_count = Payment.objects.count()
        payment_id = Payment.objects.first().id
        self.client.delete('/api/payments/{}/'.format(payment_id))
        self.assertEqual(Payment.objects.count(),initial_payment_count - 1)
        self.assertRaises(Payment.DoesNotExist,Payment.objects.get,id=payment_id)


class PaymentListTestCase(APITestCase):
    def test_list_payments(self):
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class PaymentUpdateTestCase(APITestCase):
    def setUp(self):
        self.payment = Payment.objects.create(
            payment_type = 'khalti'
        )
        return super().setUp()

    def test_update_payment(self):
        payment = Payment.objects.first()
        response = self.client.put('/api/payments/{}/'.format(payment.id),
        {
            'payment_type':'esewa',
        },
        format = 'json',
        )
        updated = Payment.objects.get(id=payment.id)
        self.assertEqual(updated.payment_type,'esewa')


class CartCreateTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email = 'test@gmail.com',
            first_name = 'test',
            last_name = 'test',
            address = 'test-11',
            phone = '987646646',
            password = 'test'
        )
        self.client.force_authenticate(self.user)
        return super().setUp()

    def test_create_cart(self):
        initial_cart_count = Cart.objects.count()
        cart_attrs = {
            'user' : self.user
        }
        response = self.client.post('/api/carts/')
        if response.status_code != 201:
            print(response.data)
        for attr, expected_value in cart_attrs.items():
            self.assertEqual(response.data[attr],expected_value.id)
        self.assertEqual(Cart.objects.count(),initial_cart_count + 1,)


class CartDestroyTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email = 'test@gmail.com',
            first_name = 'test',
            last_name = 'test',
            address = 'test-11',
            phone = '987646646',
            password = 'test'
        )
        self.client.force_authenticate(self.user)

        self.cart = Cart.objects.create(user = self.user)
        return super().setUp()

    def test_delete_cart(self):
        initial_cart_count = Cart.objects.count()
        cart_id = Cart.objects.first().id
        self.client.delete('/api/cart/{}/'.format(cart_id))
        self.assertEqual(Cart.objects.count(),initial_cart_count - 1)
        self.assertRaises(Cart.DoesNotExist,Cart.objects.get,id=cart_id)


class CartListTestCase(APITestCase):
    def test_list_cart(self):
        response = self.client.get('/api/carts/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class CartItemCreateTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email = 'test@gmail.com',
            first_name = 'test',
            last_name = 'test',
            address = 'test-11',
            phone = '987646646',
            password = 'test'
        )
        self.client.force_authenticate(self.user)

        self.cart = Cart.objects.create(
            user = self.user
        )

        self.category = Category.objects.create(
                id = 1,
                name= 'hanging',
                # 'image': "static/hanging.jpg",
                description = 'can be decorated by hanging around the house'
            )

        self.plant = Plants.objects.create(
            name = "cactus",
            unit_price = 12.0,
            suitable_temperature = "12-30",
            description = "grows in hot climate",
            category = self.category
        )

    def test_create_cart_item(self):
        initial_cart_item_count = CartItem.objects.count()
        cart_item_attrs = {
            'quantity':3,
            'cart':1,
            'plant':1
        }       
        response = self.client.post('/api/cartItems/',cart_item_attrs)
        if response.status_code != 201:
            print(response.data)
        for attr,expected_value in cart_item_attrs.items():
            self.assertEqual(response.data[attr],expected_value)
        self.assertEqual(CartItem.objects.count(),initial_cart_item_count + 1)


class CartItemDestroyTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email = 'test@gmail.com',
            first_name = 'test',
            last_name = 'test',
            address = 'test-11',
            phone = '987646646',
            password = 'test'
        )
        self.client.force_authenticate(self.user)

        self.cart = Cart.objects.create(
            user = self.user
        )

        self.category = Category.objects.create(
                id = 1,
                name= 'hanging',
                # 'image': "static/hanging.jpg",
                description = 'can be decorated by hanging around the house'
            )

        self.plant = Plants.objects.create(
            name = "cactus",
            unit_price = 12.0,
            suitable_temperature = "12-30",
            description = "grows in hot climate",
            category = self.category
        )

        self.cartItem = CartItem.objects.create(
            quantity = 3,
            cart = self.cart,
            plant = self.plant
        )

    def test_delete_cart_item(self):
        initial_cart_item_count = CartItem.objects.count()
        cart_item_id = CartItem.objects.first().id
        self.client.delete('/api/cartItems/{}/'.format(cart_item_id))
        self.assertEqual(CartItem.objects.count(), initial_cart_item_count - 1)
        self.assertRaises(CartItem.DoesNotExist,CartItem.objects.get,id = cart_item_id)


class CartItemListTestCase(APITestCase):
    def test_list_cart_items(self):
        response = self.client.get('/api/cartItems/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class CartItemUpdateTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email = 'test@gmail.com',
            first_name = 'test',
            last_name = 'test',
            address = 'test-11',
            phone = '987646646',
            password = 'test'
        )
        self.client.force_authenticate(self.user)

        self.cart = Cart.objects.create(
            user = self.user
        )

        self.category = Category.objects.create(
                id = 1,
                name= 'hanging',
                # 'image': "static/hanging.jpg",
                description = 'can be decorated by hanging around the house'
            )

        self.plant = Plants.objects.create(
            name = "cactus",
            unit_price = 12.0,
            suitable_temperature = "12-30",
            description = "grows in hot climate",
            category = self.category
        )

        self.cartItem = CartItem.objects.create(
            quantity = 3,
            cart = self.cart,
            plant = self.plant
        )

    def test_update_cart_item(self):
        cart_item = CartItem.objects.first()
        response = self.client.put('/api/cartItems/{}/'.format(cart_item.id),
        {
            'quantity' : 1,
            'cart' : 1,
            'plant':1
        }, format = 'json'
        )
        updated = CartItem.objects.get(id=cart_item.id)
        self.assertEqual(updated.quantity,1)


class OrderCreateTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
        email = 'test@gmail.com',
        first_name = 'test',
        last_name = 'test',
        address = 'test-11',
        phone = '987646646',
        password = 'test'
        )
        self.client.force_authenticate(self.user)

        self.payment = Payment.objects.create(payment_type = 'khalti')


    def test_create_order(self):
        initial_order_count = Orders.objects.count()
        order_attrs = {
            'total':'23.00',
            'payment':1,
            'delivery_address':'bharatpur-11,Chitwan'
        }

        response = self.client.post('/api/orders/',order_attrs)
        if response.status_code != 201:
            print(response.data)
        for attr, expected_value in order_attrs.items():
            self.assertEqual(response.data[attr],expected_value)
        self.assertEqual(Orders.objects.count(),initial_order_count + 1)


class OrderDestroyTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
        email = 'test@gmail.com',
        first_name = 'test',
        last_name = 'test',
        address = 'test-11',
        phone = '987646646',
        password = 'test'
        )
        self.client.force_authenticate(self.user)

        self.payment = Payment.objects.create(payment_type = 'khalti')
        self.order = Orders.objects.create(
            total = 12.00,
            user = self.user,
            payment = self.payment,
            delivery_address = 'bhratapur-11, Chitwan',
            )
    
    def test_delete_order(self):
        initial_order_count = Orders.objects.count()
        order_id = Orders.objects.first().id
        self.client.delete('/api/orders/{}/'.format(order_id))
        self.assertEqual(Orders.objects.count(),initial_order_count - 1) 
        self.assertRaises(Orders.DoesNotExist,Orders.objects.get, id=order_id,)


class OrderListTestCase(APITestCase):
    def test_list_orders(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class PlantOrderCreateTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
        email = 'test@gmail.com',
        first_name = 'test',
        last_name = 'test',
        address = 'test-11',
        phone = '987646646',
        password = 'test'
        )
        self.client.force_authenticate(self.user)

        self.payment = Payment.objects.create(payment_type = 'khalti')
        self.order = Orders.objects.create(
            total = 12.00,
            user = self.user,
            payment = self.payment,
            delivery_address = 'bhratapur-11, Chitwan',
            )

        self.category = Category.objects.create(
                id = 1,
                name= 'hanging',
                # 'image': "static/hanging.jpg",
                description = 'can be decorated by hanging around the house'
            )

        self.plant = Plants.objects.create(
            name = "cactus",
            unit_price = 12.0,
            suitable_temperature = "12-30",
            description = "grows in hot climate",
            category = self.category
        )

    def test_create_plant_order(self):
        initial_plant_order_count = PlantOrder.objects.count()
        plant_order_attrs = {
            'quantity':2,
            'total':'12.00',
            'order':1,
            'plant':1
        }
        response = self.client.post('/api/plantOrder/',plant_order_attrs)
        if response.status_code != 201:
            print(response.data)
        for attr, expected_value in plant_order_attrs.items():
            self.assertEqual(response.data[attr],expected_value)
        self.assertEqual(PlantOrder.objects.count(),initial_plant_order_count + 1)


class PlantOrderListTestCase(APITestCase):
    def test_plant_order(self):
        response = self.client.get('/api/plantOrder/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UsersPlantCreateTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
        email = 'test@gmail.com',
        first_name = 'test',
        last_name = 'test',
        address = 'test-11',
        phone = '987646646',
        password = 'test'
        )
        self.client.force_authenticate(self.user)

        self.category = Category.objects.create(
                id = 1,
                name= 'hanging',
                # 'image': "static/hanging.jpg",
                description = 'can be decorated by hanging around the house'
            )

        self.plant = Plants.objects.create(
            name = "cactus",
            unit_price = 12.0,
            suitable_temperature = "12-30",
            description = "grows in hot climate",
            category = self.category
        )

    def test_create_usersplant(self):
        initial_users_plant_count = UserPlant.objects.count()
        users_plant_attrs = {
            'user_id':1,
            'plant_id':1
        }
        response = self.client.post('/api/user/plants/',users_plant_attrs)
        if response.status_code != 201:
            print(response.data)
        for attr,expected_value in users_plant_attrs.items():
            self.assertEqual(response.data[attr],expected_value)
        self.assertEqual(UserPlant.objects.count(),initial_users_plant_count + 1)
        

class UsersPlantListTestCase(APITestCase):
    def test_list_users_plants(self):
        response = self.client.get('/api/user/plants/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class UserDeviceTokenCreateTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
        email = 'test@gmail.com',
        first_name = 'test',
        last_name = 'test',
        address = 'test-11',
        phone = '987646646',
        password = 'test'
        )
        self.client.force_authenticate(self.user)
    
    def test_create_user_device_token(self):
        initial_user_device_token = UserDeviceToken.objects.count()
        user_device_token_attrs = {
            'user_id':1,
            'token':'a long token'
        }
        response = self.client.post('/api/userdevice/',user_device_token_attrs)
        if response.status_code != 201:
            print(response.data)
        for attr, expected_value in user_device_token_attrs.items():
            self.assertEqual(response.data[attr],expected_value)
        self.assertEqual(UserDeviceToken.objects.count(),initial_user_device_token + 1)


class UserDeviceTokenDestroyTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
        email = 'test@gmail.com',
        first_name = 'test',
        last_name = 'test',
        address = 'test-11',
        phone = '987646646',
        password = 'test'
        )
        self.client.force_authenticate(self.user)

        self.userDeviceToken = UserDeviceToken.objects.create(
            user_id = self.user,
            token = 'a long token'
        )
        return super().setUp()

    def test_delete_user_device_token(self):
        initial_user_device_token_count = UserDeviceToken.objects.count()
        user_device_token_id = UserDeviceToken.objects.first().id
        self.client.delete('/api/userdevice/{}/'.format(user_device_token_id))
        self.assertEqual(UserDeviceToken.objects.count(),initial_user_device_token_count - 1)
        self.assertRaises(UserDeviceToken.DoesNotExist,UserDeviceToken.objects.get,id=user_device_token_id)


class UserDeviceTokenListTestCase(APITestCase):
    def test_list_user_device_token(self):
        response = self.client.get('/api/userdevice/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class RegisterUserTestCase(APITestCase):
    def test_create_user(self):
        initial_user_count = CustomUser.objects.count()
        user_attrs = {
            'email':'test@gmail.com',
            'password':'test@123',
            'password2':'test@123',
            'first_name':'test',
            'last_name':'test',
            'address':'bharatpur-11',
            'phone':'9872536273',
        }
        response = self.client.post('/api/register/',user_attrs)
        if response.status_code != 201:
            print(response.data)       
        self.assertEqual(CustomUser.objects.count(), initial_user_count + 1)     


class LoginUserTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
        email = 'test@gmail.com',
        first_name = 'test',
        last_name = 'test',
        address = 'test-11',
        phone = '987646646',
        password = 'test@123'
        )
        # self.client.force_authenticate(self.user)
        return super().setUp()
        
    def test_login_user(self):
        user_credentials = {
            'email':'test@gmail.com',
            'password':'test@123'
        }
        response = self.client.post('/api/token/',user_credentials, format = 'json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class LogoutUserTestCase(APITestCase):
    
    def test_logout_user(self):
        self.user = CustomUser.objects.create_user(
        email = 'test@gmail.com',
        first_name = 'test',
        last_name = 'test',
        address = 'test-11',
        phone = '987646646',
        password = 'test@123'
        )
        self.client.force_authenticate(self.user)
        user_credentials = {
            'email':'test@gmail.com',
            'password':'test@123'
        }
        login_response = self.client.post('/api/token/',user_credentials, format = 'json')
        refresh_token = login_response.data['refresh']

        logout_attrs = {
            'refresh_token':refresh_token
        }
        response = self.client.post('/api/logout/',logout_attrs)
        self.assertEqual(response.status_code,status.HTTP_205_RESET_CONTENT)

