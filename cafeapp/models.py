from django.db import models

# 手順3
class Reservation(models.Model):
    id = models.AutoField(primary_key=True)  # 自動的に連番で登録されるフィールド。
    name = models.CharField(max_length=50)
    reservation_datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    stay_times = models.IntegerField(default=0)
    remarks = models.CharField(max_length=200, blank=True)
    is_preorder = models.IntegerField(default=0)  # 事前注文の有無を表す。「有」=1,「無」=0