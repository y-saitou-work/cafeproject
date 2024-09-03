from django.shortcuts import render
from django.views.generic import ListView, DetailView, View#  手順2-3で追加
from .models import Reservation
from datetime import datetime, date, timedelta, time#  手順2-3で追加
from django.db.models import Q#  手順2-3で追加
from django.utils.timezone import localtime, make_aware#  手順2-3で追加

 # 手順1-5にて追加
class ReservationListView(ListView):
    model = Reservation
    paginate_by = 20

 # 手順1-6にて追加
class ReservationDetailView(DetailView):
    model = Reservation

#  手順2-3で追加
class CalendarView(View):
    def get(self, request, *args, **kwargs):  
        #*args: 複数の引数をタプルとして受け取る。**kwargs: 複数のキーワード引数を辞書として受け取る
        customer_data = Reservation.objects.filter(id=self.kwargs['pk']).select_related('customer')[0].customer # 変更
        today = date.today()
        year = self.kwargs.get('year')  # kwargsで渡された、キーがyearの値をURLからGET
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if year and month and day:  # 日付がURLで指定された場合は、その日をstart_dateへ指定する。
            # 週初め
            start_date = date(year=year, month=month, day=day)
        else:  # 日付がURLで指定されtていない場合は、本日をstart_dateへ指定する。
            start_date = today
        
        # 1週間の日付ｗリストにする
        days = [start_date + timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]  #1週間の最後の日

        calendar = {}
        # 10時～16時
        for hour in range(10, 16):
            row = {}
            for day in days:
                row[day] = True  # row[12/3]=True,row[12/4]=True...
            calendar[hour] = row  #2次元配列で、 1週間、それぞれ日の営業時間にTrueを入れている
        start_time = make_aware(datetime.combine(start_day, time(hour=10, minute=0, second=0)))  #開始時間(ex:12/3 10:00:00 )を設定
        end_time = make_aware(datetime.combine(end_day, time(hour=16, minute=0, second=0)))  #終了時間を作成
        
        reservation_data = Reservation.objects.filter(customer=customer_data).exclude(Q(datetime__gt=end_time) | Q(end_datetime__lt=start_time))  # 顧客の予約状況を取得
          # Qクエリで、AND、OR条件が作成できる。この場合は、開始時間＜終了時間、終了時間＜開始時間の場合を除外している。
        # for reservation in reservation_data:
        #     local_time = localtime(reservation.start)  # 現地のタイムゾーンを取得
        #     reservation_date = local_time.date()  #現地の日時を取得
        #     reservation_hour = local_time.hour
        #     if (reservation_hour in calendar) and (reservation_date in calendar[reservation_hour]):
        #         calendar[reservation_hour][reservation_date] = False  #予約の日時の二次元配列をFにすることで、予約を設定している。
        
        return render(request, 'cafeapp/calendar.html', {
            'customer_data': customer_data,
            'calendar': calendar,
            'days': days,
            'start_day': start_day,
            'end_day': end_day,
            'before': days[0] - timedelta(days=7),
            'next': days[-1] + timedelta(days=1),
            'today': today,
        })
