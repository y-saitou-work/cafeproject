"""cafeproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cafeapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 手順1-5にて追加
    path('reservation/list/',views.ReservationListView.as_view(), name='reservation_list'),
    # 手順1-7にて追加
    path('reservation/detail/<int:pk>', views.ReservationDetailView.as_view(), name='reservation_detail'),
    # 手順2-2
    path('calendar/', views.CalendarView.as_view(), name='calendar'),  # 日にちが指定されていない場合
    path('calendar/<int:year>/<int:month>/<int:day>/', views.CalendarView.as_view(), name='calendar'),  # 日にちが指定された場合
    # 手順3-1
    path('reserve/<int:year>/<int:month>/<int:day>/<int:hour>', views.ReservationView.as_view(), name='reserve')
]
