from django.shortcuts import render
from django.views.generic import ListView, DetailView, View#  手順2-3で追加
from .models import Reservation
from datetime import datetime, date, timedelta, time#  手順2-3で追加
from django.db.models import Q#  手順2-3で追加
from django.utils.timezone import localtime, make_aware#  手順2-3で追加
from .forms import ReservationForm


SEAT_NUM = 5  # 席数

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
        #customer_data = Reservation.objects.filter(id=self.kwargs['pk']).select_related('customer')[0].customer # 変更
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
        booked_seat = {}  #各日時の予約済み席数 
        # 10時～16時
        for hour in range(10, 17):
            row_calendar = {}
            row_seat = {}
            for day in days:
                row_calendar[day] = True  # row[12/3]=True,row[12/4]=True...
                row_seat[day] = 0  # 全ての日に0を入れている
            calendar[hour] = row_calendar  #2次元配列で、 1週間、それぞれ日の営業時間にTrueを入れている
            booked_seat[hour] = row_seat  # 同じく2次元配列で、全てに0を入れる
        
        start_time = make_aware(datetime.combine(start_day, time(hour=10, minute=0, second=0)))  #開始時間(ex:12/3 10:00:00 )を設定
        end_time = make_aware(datetime.combine(end_day, time(hour=17, minute=0, second=0)))  #終了時間を作成(最終枠が16：00～17：00なので、endtimeは17:00)
        
        reservation_data = Reservation.objects.filter(datetime__gte=start_time, end_datetime__lte=end_time) # 日時がstart_datetime~enddatetimeまでの予約を抽出。
          # 利用開始時間>=カレンダーの始まり日時、利用終了時間<=カレンダーの終わり日時の場合を取得
        
        # その時間に、一つでも予約があったら✖を付けるパターン
        for reservation in reservation_data: # 予約情報を1件づつreservationへ
            local_time = localtime(reservation.datetime)  # 現地のタイムゾーンでの日時を取得
            reservation_date = local_time.date()  #現地の日時を取得
            reservation_hour = local_time.hour
            if booked_seat[reservation_hour][reservation_date] <= SEAT_NUM :  # まだ空席があったら
               booked_seat[reservation_hour][reservation_date] = booked_seat[reservation_hour][reservation_date] + 1
            else: # 空席が無い場合、次のIF文を実行する必要が無いため、nextし、次のループへ
                next

            if booked_seat[reservation_hour][reservation_date] ==SEAT_NUM:
                calendar[reservation_hour][reservation_date] = False  #予約の日時の二次元配列をFにすることで、予約を設定している。
        
        return render(request, 'cafeapp/calendar.html', {
            'calendar': calendar,
            'days': days,
            'start_day': start_day,
            'end_day': end_day,
            'before': days[0] - timedelta(days=7),
            'next': days[-1] + timedelta(days=1),
            'today': today,
        })

class ReservationView(View):
    def get(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        form =ReservationForm(request.POST or None)
        return render(request,'reservation.html',{
            'year':year,
            'month': month,
            'day': day,
            'hour': hour,
            'form': form,
        })
    
    def post(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))
        end_time = make_aware(datetime(year=year, month=month, day=day, hour=hour + 1))
        reservation_data = Reservation.objects.filter(year=year, month=month, day=day, hour=hour, start_time=start_time)
        form = ReservationForm(request.POST or None)
        if len(reservation_data) ==  SEAT_NUM:
            form.add_error(None, '満席です。\n別の日時で予約をお願いします。')
        else:
            if form.is_valid():
                reservation = Reservation()
                reservation.datetime = start_time 
                reservation.end_datetime = end_time
                reservation.customer_name = form.cleaned_data['customer_name']
                