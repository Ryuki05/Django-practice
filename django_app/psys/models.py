from django.db import models


# 得意先採番テーブル
class CustomerNumbering(models.Model):
    customer_code = models.PositiveIntegerField(primary_key=True)  # 数値型、4桁

    class Meta:
        db_table = "customer_numbering"


# 得意先テーブル
class Customer(models.Model):
    customer_code = models.CharField(primary_key=True, max_length=6)  # テキスト型、6桁
    name = models.CharField(max_length=32)  # 得意先名称
    phone_number = models.CharField(max_length=13)  # 電話番号
    postal_code = models.CharField(max_length=8)  # 郵便番号
    address = models.CharField(max_length=40)  # 住所
    discount_rate = models.PositiveSmallIntegerField()  # 割引率
    delete_flag = models.BooleanField(default=False)  # 削除フラグ

    class Meta:
        db_table = "customer"


# 従業員テーブル
class Employee(models.Model):
    employee_number = models.CharField(primary_key=True, max_length=6)  # 従業員番号
    name = models.CharField(max_length=32)  # 従業員名
    password = models.CharField(max_length=6)  # パスワード

    class Meta:
        db_table = "employee"


# 商品テーブル
class Item(models.Model):
    item_code = models.CharField(primary_key=True, max_length=6)  # 商品コード
    name = models.CharField(max_length=32)  # 商品名称
    price = models.PositiveIntegerField()  # 単価
    stock = models.PositiveIntegerField()  # 在庫数

    class Meta:
        db_table = "item"


# 受注テーブル
class Orders(models.Model):
    order_number = models.CharField(primary_key=True, max_length=6)  # 受注番号
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # 外部キー: 得意先コード
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # 外部キー: 従業員番号
    total_amount = models.PositiveIntegerField()  # 受注合計金額
    detail_count = models.PositiveSmallIntegerField()  # 受注明細件数
    delivery_date = models.DateField()  # 納入日
    order_date = models.DateField()  # 受注日

    class Meta:
        db_table = "orders"


# 受注明細テーブル
class OrderDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)  # 外部キー: 受注番号
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # 外部キー: 商品コード
    order_quantity = models.PositiveIntegerField()  # 受注数量
    order_amount = models.PositiveIntegerField()  # 受注金額

    class Meta:
        db_table = "order_details"
        unique_together = (('order', 'item'),)


# Django標準のテーブルはそのまま使用します。
# Auth関連、Adminログ、セッション、マイグレーションテーブル
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "auth_user"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"
