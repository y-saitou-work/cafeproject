from django.db import models
from django.utils import timezone  #手順2-1追加


# 手順2-1
class Customer(models.Model):
    id = models.AutoField(primary_key=True)  # 自動的に連番で登録されるフィールド。
    name = models.CharField(max_length=50)  #　TODOReservationクラスから外部参照されるようにする

# 手順1-3
class Reservation(models.Model):
    id = models.AutoField(primary_key=True)  # 自動的に連番で登録されるフィールド。
    customer_name = models.CharField(max_length=50)  #TODO Customerを外部参照
    phone_number = models.CharField(max_length=11)  # 手順5にて追加
    datetime = models.DateTimeField(default=timezone.now)  # 変更
    end_datetime = models.DateTimeField(default=timezone.now) # 手順2-1で追加。カフェの利用終了予定時間
    stay_times = models.PositiveIntegerField(default=0)  # 正の数のみ入力できるよう変更
    remarks = models.CharField(max_length=200, blank=True)
    is_preorder = models.PositiveIntegerField(default=0)  # 事前注文の有無を表す。「有」=1,「無」=0

    # 日時の変数を、 YYYY/MM/DD hh:mm形式に書式化して表示する変数
    def __str__(self):
        return str(self.id)

class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

class Menu(models.Model):
    menu_name = models.CharField(max_length=80)
    price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Categoryが削除されたら、結びついているProductも削除される設定

class MenuSelected(models.Model):
    menus = models.ManyToManyField(Menu)  # 多対多の関係
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    # メニュー名はManyToManyFieldなので、MenuSelectedが複数もっている。それら全て表示するため、カンマ区切りで表示するメソッドを追加
    def get_menus(self):
        return ", ".join([menu.menu_name for menu in self.menus.all()])

    get_menus.short_description = "Menus"  # 管理サイトでの表示名を設定








