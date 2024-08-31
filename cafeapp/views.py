from django.shortcuts import render
from django.views.generic import ListView
from .models import Reservation

 # 手順5にて追加
class ReservationListView(ListView):
    model = Reservation
    paginate_by = 20
