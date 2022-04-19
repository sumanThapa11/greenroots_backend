from django.contrib import admin

from plants.models import *

Models = (CustomUser,Category,Payment,Plants,Orders,Cart,CartItem,PlantOrder)

admin.site.register(Models)
