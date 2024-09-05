from django.db import models
from django.utils import timezone  #手順2-1追加


# 手順2-1
class Customer(models.Model):
    id = models.AutoField(primary_key=True)  # 自動的に連番で登録されるフィールド。
    name = models.CharField(max_length=50)  #　TODOReservationクラスから外部参照されるようにする

# 手順1-3
class Reservation(models.Model):
    id = models.AutoField(primary_key=True)  # 自動的に連番で登録されるフィールド。
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)  #変更
    customer_name = models.CharField(max_length=50)  #TODO Customerを外部参照
    datetime = models.DateTimeField(default=timezone.now)  # 変更
    end_datetime = models.DateTimeField(default=timezone.now) # 手順2-1で追加。カフェの利用終了予定時間
    stay_times = models.IntegerField(default=0)
    remarks = models.CharField(max_length=200, blank=True)
    is_preorder = models.IntegerField(default=0)  # 事前注文の有無を表す。「有」=1,「無」=0

    # 日時の変数を、 YYYY/MM/DD hh:mm形式に書式化して表示する変数
    def __str__(self):
        datetime = timezone.localtime(self.datetime).strftime('%Y/%m/%d %H:%M')
        end_datetime = timezone.localtime(self.end_datetime).strftime('%Y/%m/%d %H:%M')
        return f'{datetime} ~ {end_datetime}'  # 変更


