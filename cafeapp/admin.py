from django.contrib import admin
from .models import Reservation, Menu, Category, MenuSelected  # 追加変更(Customerを削除)

# 手順1-3にて追加
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id','customer_name','datetime', 'is_preorder')
    search_fields = ('customer_name','datetime')

admin.site.register(Reservation,ReservationAdmin)

# 手順3で作成
class MenuAdmin(admin.ModelAdmin):
    list_display = ('menu_name', 'price','category', )
    search_fields = ('menu_name','category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category_name')
    
class MenuSelectedAdmin(admin.ModelAdmin):  # 手順3-5で追加
    list_display = ('get_menus', 'reservation', 'quantity')


admin.site.register(Menu, MenuAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(MenuSelected, MenuSelectedAdmin)