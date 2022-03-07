"""greenroots URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)

from django.conf.urls.static import static
from django.conf import settings

from plants.views import CartItemList, CartList, OrderList, PaymentList, PlantList, RegisterUser,LogoutUser,CategoryList,UsersCart,PlantOrderList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterUser.as_view(), name='register_user'),
    path('api/logout/', LogoutUser.as_view(), name='logout_user'),

    #CRUD category
    path('api/category/', CategoryList.as_view(), name='categories'),
    path('api/category/<int:pk>/', CategoryList.as_view(), name='category'),

    #CRUD plants
    path('api/plants/', PlantList.as_view(), name='plants'),
    path('api/plants/<int:pk>/', PlantList.as_view(), name='plant'),

    #CRUD cart
    path('api/carts/', CartList.as_view(), name='carts'),
    path('api/cart/<int:pk>/', CartList.as_view(), name='cart'),

    path('api/user/cart/', UsersCart.as_view(), name='users cart'),

    #CRUD cart_item
    path('api/cartItems/', CartItemList.as_view(), name='cart_items'),
    path('api/cartItems/<int:pk>/', CartItemList.as_view(), name='cart_item'),

    #CRUD orders
    path('api/orders/',OrderList.as_view(),name='orders'),
    path('api/orders/<int:pk>/',OrderList.as_view(),name='order'),

    #CRYD plantOrder
    path('api/plantOrder/',PlantOrderList.as_view(),name='plantOrder'),


    #CRUD payments
    path('api/payments/',PaymentList.as_view(),name='payments'),
    

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


