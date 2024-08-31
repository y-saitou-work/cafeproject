from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Reservation

 # 手順5にて追加
class ReservationListView(ListView):
    model = Reservation
    paginate_by = 20

 # 手順6にて追加
class ReservationDetailView(DetailView):
    model = Reservation