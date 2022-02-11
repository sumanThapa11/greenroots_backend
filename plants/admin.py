from django.contrib import admin

from plants.models import *

Models = (CustomUser,Category,Payment,Plants,PlantImage,Cart,CartItem,Orders,PlantOrder)

admin.site.register(Models)
