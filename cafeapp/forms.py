from django import forms

class ReservationForm(forms.Form):
    customer_name = forms.CharField(max_length=50, label='お名前')
    stay_times = forms.IntegerField(label='滞在時間(1時間単位)')
    remarks = forms.CharField(max_length=200, label='備考')
    is_preorder = forms.IntegerField(label='事前注文(有り=1、無し=0で記入)')  # 事前注文の有無を表す。「有」=1,「無」=0