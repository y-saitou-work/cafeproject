from typing import Any, Mapping
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from .models import Menu, MenuSelected

class ReservationForm(forms.Form):
    customer_name = forms.CharField(max_length=50, label='お名前')
    stay_times = forms.IntegerField(label='滞在時間(1時間単位)')
    remarks = forms.CharField(max_length=200, label='備考', required=False)  # 空欄でも予約できるよう、required=Falseとした。
    is_preorder = forms.IntegerField(label='事前注文(有り=1、無し=0で記入)')  # 事前注文の有無を表す。「有」=1,「無」=0

class MenuSelectedForm(forms.Form):
    def __init__(self, *args, **kwargs):  # このクラスが呼び出されたら、自動的に最初に行うメソッド
        super().__init__(*args, **kwargs)
        menus = Menu.objects.all()  # 全てのメニューを取得
        for menu in menus:
            # 各メニュー名に対応した数量フィールドを作成する
            self.fields[f'{menu.menu_name}'] = forms.IntegerField(
                label = menu.menu_name,
                min_value=0,  # 0以上の数値のみ許可
                initial=0,   # デフォルト値を0に設定
                required=False  # 数量が入力されていない場合は無視
            )
