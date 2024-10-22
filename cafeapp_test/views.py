from django.shortcuts import render, redirect # 手順3で追加
from django.views.generic import ListView, DetailView, View, TemplateView, UpdateView, DeleteView, CreateView  #  手順2-3,5,8,9,11で追加
from .models import Reservation, Menu, MenuSelected  # 手順3-6で追加
from datetime import datetime, date, timedelta, time#  手順2-3で追加
from django.db.models import Q#  手順2-3で追加
from django.utils.timezone import localtime, make_aware  # 手順2-3で追加
from .forms import ReservationForm, MenuSelectedForm # 手順3で追加
from django.http import HttpResponseRedirect  # 手順4で追加
from django.urls import reverse, reverse_lazy


SEAT_NUM = 5  # 席数を定数に保存

 # 手順1-5にて追加
class ReservationListView(ListView):
    model = Reservation
    paginate_by = 20

 # 手順1-6にて追加
class ReservationDetailView(DetailView):
    model = Reservation

    # 手順10にて、事前注文が表示できるように追加
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservaion = self.get_object() # 現在の予約を取得
        context['menu_selected_items'] = MenuSelected.objects.filter(reservation=reservaion)
        return context


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
        else:  # 日付がURLで指定されていない場合は、本日をstart_dateへ指定する。
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
        
        # 各日時の予約数をカウント、満席であればFalseを入れる
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
    # getメソッド...主にデータの取得や表示を行います。フォームやページを表示する際に使われ、ユーザーが特定のリソースを要求した際に、そのリソース（HTMLページやデータ）を返す役割があります。
    # 例えば、予約ページを開いてメニューの一覧を表示したり、指定された日付の情報を表示する処理に使われます。
    def get(self, request, *args, **kwargs):
        """予約フォームと、事前注文用のメニュー選択フォームを表示する"""
        # kwargsから日付情報を取得
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        hour = self.kwargs.get('hour')
        # TODO　下記の引数の意味
        reservation_form =ReservationForm(request.POST or None)  # 予約フォームを取得
        menu_selected_form = MenuSelectedForm()  #手順3-6 MenuSelectedFormも取得

        # メニューと価格を取得してテンプレートに渡す
        menus_with_prices = Menu.objects.all().values('menu_name', 'price')  # メニュー名と価格を取得

        # コンテキストデータを作成してテンプレートへ渡す
        context = {
            'year':year,
            'month': month,
            'day': day,
            'hour': hour,
            'menus_with_prices' : menus_with_prices,
            'form': reservation_form, # TODOcontextの中にフォームを入れて大丈夫？
            'menu_selected_form': menu_selected_form,  #手順3-6 MenuSelectedFormをテンプレートに渡す
        }

        return render(request, 'cafeapp/reserve.html', context)

    # postメソッド...主にデータの送信や処理を行います。ユーザーがフォームを送信した際に、そのデータを受け取り、データベースに保存したり、処理を行う際に使われます。
    # 予約フォームを送信して新しい予約を作成したり、選択されたメニューを保存する処理に使われます。
    def post(self, request, *args, **kwargs):
        # 予約データを保存し、関連するメニューも保存する
        #URLで渡された日時情報を受け取り
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))

        reservation = self.create_reservation(request, start_time)
        
        return self.redirect_to_confirmation(start_time, reservation)
        
    
    def create_reservation(self, request, start_time):
        """予約ページに入力された内容から予約情報を作成して保存する"""
        reservation_form = ReservationForm(request.POST) 
        menu_selected_form = MenuSelectedForm(request.POST)  #手順3-6 POSTされたデータをMenuSelectedFormに渡
        reservation_data = Reservation.objects.filter(datetime=start_time)
        
        if len(reservation_data) == SEAT_NUM: # もしも、calenderにアクセスしてからreservationに遷移する間に選択した日時が満席になった場合
            reservation_form.add_error(None, '満席です。\n別の日時で予約をお願いします。')
            return None
        
        if reservation_form.is_valid() and menu_selected_form.is_valid():  # 両方のフォームが有効か確認
            reservation = Reservation.objects.create(
                    customer_name=reservation_form.cleaned_data['customer_name'],
                    phone_number=reservation_form.cleaned_data['phone_number'],
                    datetime=start_time,
                    stay_times=reservation_form.cleaned_data['stay_times'],
                    end_datetime=start_time + timedelta(hours=reservation_form.cleaned_data['stay_times']),
                    remarks=reservation_form.cleaned_data['remarks'],
                    is_preorder=reservation_form.cleaned_data['is_preorder']
            )

            # 「事前注文あり」が1だった場合は、メニューを保存するsave_selected_menusメソッドへ
            if reservation_form.cleaned_data['is_preorder'] == 1: 
                self.save_selected_menus(request, reservation,menu_selected_form)
            return reservation
        else:
            return None # フォームが無効の場合もNoneを返す

    def save_selected_menus(self, request, reservation, menu_selected_form):
        """選択されたメニューを保存する"""
        # menu_selected_form.cleaned_data=バリデーションをクリアしたものだけを辞書形式で格納したもの
        for menu_name, quantity in menu_selected_form.cleaned_data.items():
            if quantity > 0:
                try:
                    menu = Menu.objects.get(menu_name=menu_name)
                    
                    menu_selected = MenuSelected.objects.create(
                        reservation=reservation,
                        quantity=quantity
                    )
                    
                    menu_selected.menus.add(menu)  # ManyToManyの関係にメニューを追加
                    menu_selected.save()
                except Menu.DoesNotExist:
                    print(f"{menu_name} が存在しません")

    def redirect_to_confirmation(self, start_time,reservation):
        """予約完了後、予約番号と顧客名をGETパラメータに含めたURLにリダイレクトします。"""
        return HttpResponseRedirect(reverse('reserve_complete', kwargs={
            'datetime' : start_time.strftime("%Y-%m-%d-%H-%M"),  # URLで使用するフォーマットに合わせる
            'customer_name' : reservation.customer_name
        }))

    
# 手順4
class ReserveCompleteView(View):
   def get(self, request, *args, **kwargs):  
        #*args: 複数の引数をタプルとして受け取る。**kwargs: 複数のキーワード引数を辞書として受け取る
        datetime_str = self.kwargs.get('datetime')
        customer_name = self.kwargs.get('customer_name')

        # 予約情報テーブル(Reservationモデル)から、getされた日時・名前の予約番号を取得する。
        ## ハイフン区切りの文字列を datetime オブジェクトに変換する
        start_time = datetime.strptime(datetime_str, "%Y-%m-%d-%H-%M")
        # タイムゾーンを考慮して aware な datetime オブジェクトに変換する
        start_time_aware = make_aware(start_time)
        # Reservation モデルから datetime と customer_name で検索する。
        # datetime と customer_nameの組み合わせで複数ある場合は、最新のものを選択
        reservation_info = Reservation.objects.filter(
            datetime=start_time_aware, customer_name=customer_name
        ).latest('id')
        # レコードから予約番号を取得
        reservation_num = reservation_info.id

        return render(request,'cafeapp/reserve_complete.html',{
            'datetime' : start_time.strftime("%Y-%m-%d %H:%M"),
            'customer_name' : customer_name,
            'reservation_num' : reservation_num
        })
   
class ReservationError(View):
    template_name = "cafeapp/reservation_error.html"

class TopView(TemplateView):
    template_name = "cafeapp/top.html"

class CustomerReservationListView(ListView):
    model = Reservation
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        # POSTリクエストで送信された名前を取得
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        # クエリセットをフィルタリング
        queryset = Reservation.objects.filter(customer_name=name, phone_number=phone_number)
        # フィルタリングされたクエリセットを手動でself.object_list
        self.object_list = queryset
        # self.object_listに設定したクエリセットを使ってコンテキストを作成し、テンプレートに渡す
        context = super().get_context_data(object_list=self.object_list) 

        return self.render_to_response(context)

# 手順8で追加
class ReservationUpdateView(UpdateView):
    model= Reservation
    fields = '__all__' # ユーザーが入力するフィールドを指定する
    template_name_suffix = '_update_form'  # 編集用のTemplateファイル名を指定。この場合はproduct_update_form.htmlとなる

#手順9で追加
class ReservationDeleteView(DeleteView):
    model = Reservation
    success_url = reverse_lazy('top')  # 削除成功したら、top画面へ遷移

# 手順10
class EmployeeTopView(TemplateView):
    template_name = "cafeapp/employee_top.html"

# 手順11
class MenuCreateView(CreateView):
    model = Menu
    fields = '__all__' # 新規作成時にユーザーが入力するフィールドを指定する

# 手順12
class MenuListView(ListView):
    model = Menu
   
#手順13
class MenuUpdateView(UpdateView):
    model = Menu
    fields = '__all__' # ユーザーが編集するフィールドを指定する
    template_name_suffix='_update_form' # 編集用のTemplateファイル名を指定。この場合はmenu_update_form.htmlとなる

# 手順14
class MenuDeleteView(DeleteView):
    model = Menu
    success_url = reverse_lazy('menu_list')  # 削除成功したら、top画面へ遷移