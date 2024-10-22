from cafeapp_test.models import Menu, Category  # Categoryモデルをインポート

# カテゴリ名と対応するインスタンスを辞書で保持
category_names = {
    "ホットドリンク": Category.objects.get_or_create(category_name="ホットドリンク")[0],
    "アイスドリンク": Category.objects.get_or_create(category_name="アイスドリンク")[0],
    "軽食": Category.objects.get_or_create(category_name="軽食")[0],
    "期間限定": Category.objects.get_or_create(category_name="期間限定")[0],
}


menu_items = [
    {"menu_name": "ティー", "price": 350, "category": "ホットドリンク"},
    {"menu_name": "カフェラテ", "price": 390, "category": "ホットドリンク"},
    {"menu_name": "ブレンドコーヒー", "price": 300, "category": "ホットドリンク"},
    {"menu_name": "アイスコーヒー", "price": 300, "category": "アイスドリンク"},
    {"menu_name": "アイスティー", "price": 310, "category": "アイスドリンク"},
    {"menu_name": "タピオカミルクティー", "price": 550, "category": "アイスドリンク"},
    {"menu_name": "ジャーマンドッグ", "price": 220, "category": "軽食"},
    {"menu_name": "野菜サンド", "price": 220, "category": "軽食"},
    {"menu_name": "トースト", "price": 260, "category": "軽食"},
    {"menu_name": "チーズトースト", "price": 190, "category": "軽食"},
    {"menu_name": "大豆ミートサンド", "price": 250, "category": "軽食"},
    {"menu_name": "サンドウィッチ", "price": 350, "category": "軽食"},
    {"menu_name": "ジンジャーマンクッキー", "price": 150, "category": "期間限定"},
    {"menu_name": "ホットアップルティー", "price": 400, "category": "期間限定"},
    {"menu_name": "グラタンポットパイ", "price": 500, "category": "期間限定"},
]

# 一括でデータを作成
for item in menu_items:
    category_instance = category_names[item["category"]]
    Menu.objects.create(menu_name=item["menu_name"], price=item["price"], category=category_instance)