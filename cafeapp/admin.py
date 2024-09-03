from django.contrib import admin
from .models import Reservation, Customer 

# 手順3にて追加
admin.site.register(Reservation)
admin.site.register(Customer)
