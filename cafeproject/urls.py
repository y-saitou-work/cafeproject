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
    # 手順8
    path('reservation/update/<int:pk>', views.ReservationUpdateView.as_view(), name='reservation_update'),
    #手順9
    path('reservation/delete/<int:pk>', views.ReservationDeleteView.as_view(), name='reservation_delete'),
    # 手順2-2
    path('calendar/', views.CalendarView.as_view(), name='calendar'),  # 日にちが指定されていない場合
    path('calendar/<int:year>/<int:month>/<int:day>/', views.CalendarView.as_view(), name='calendar'),  # 日にちが指定された場合
    # 手順3-1
    path('reserve/<int:year>/<int:month>/<int:day>/<int:hour>', views.ReservationView.as_view(), name='reserve'),
    # 手順4
    path('reserve_complete/<str:datetime>/<str:customer_name>', views.ReserveCompleteView.as_view(), name='reserve_complete'),
    # 手順5
    #path('top/',views.TopView.as_view(), name='top'),
    path('',views.TopView.as_view(), name='top'),  # URL先が指定されなければ、自動的にTOPページが表示されるようにする
    path('customer_reservation_list/', views.CustomerReservationListView.as_view(), name='customer_reservation_list'),
    # 手順10
    path('employee_top/',views.EmployeeTopView.as_view(), name='employee_top'),
    # 手順11
    path('menu_create/',views.MenuCreateView.as_view(), name='menu_create'),
    # 手順12
    path('menu_list/', views.MenuListView.as_view(), name='menu_list'),
    # 手順13
    path('menu_update/<int:pk>', views.MenuUpdateView.as_view(), name='menu_update'),
    # 手順14
    path('menu_delete/<int:pk>', views.MenuDeleteView.as_view(), name='menu_delete'),
]