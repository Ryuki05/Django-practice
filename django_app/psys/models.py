from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class EmployeeManager(BaseUserManager):
    def create_user(self, employee_number, name, password=None):
        if not employee_number:
            raise ValueError('従業員番号は必須です')
        
        user = self.model(
            employee_number=employee_number,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, employee_number, name, password=None):
        user = self.create_user(
            employee_number=employee_number,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Employee(AbstractBaseUser, PermissionsMixin):
    employee_number = models.CharField('従業員番号', max_length=12, primary_key=True)
    name = models.CharField('従業員名', max_length=32)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField('登録日', default=timezone.now)

    objects = EmployeeManager()

    USERNAME_FIELD = 'employee_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

class CustomerNumbering(models.Model):
    customer_code = models.PositiveIntegerField(primary_key=True)

    class Meta:
        db_table = 'customer_numbering'

class Customer(models.Model):
    customer_code = models.CharField('得意先コード', max_length=10, primary_key=True)
    customer_name = models.CharField('得意先名', max_length=100)
    customer_telno = models.CharField('電話番号', max_length=20, null=True, blank=True)
    customer_postalcode = models.CharField('郵便番号', max_length=8, null=True, blank=True)
    customer_address = models.CharField('住所', max_length=200, null=True, blank=True)
    discount_rate = models.DecimalField('割引率', max_digits=5, decimal_places=2, default=0)
    delete_flag = models.BooleanField('削除フラグ', default=False)

    def __str__(self):
        return self.customer_name

class Item(models.Model):
    item_code = models.CharField('商品コード', max_length=10, primary_key=True)
    item_name = models.CharField('商品名', max_length=100)
    price = models.IntegerField('単価', default=0)
    stock_quantity = models.IntegerField('在庫数', default=0)
    delete_flag = models.BooleanField('削除フラグ', default=False)

    def __str__(self):
        return self.item_name

class Orders(models.Model):
    order_number = models.CharField('受注番号', max_length=10, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name='得意先')
    order_date = models.DateField('受注日', default=timezone.now)
    delivery_date = models.DateField('納期', null=True, blank=True)
    delete_flag = models.BooleanField('削除フラグ', default=False)

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name = '受注'
        verbose_name_plural = '受注'

class OrderDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name='商品')
    order_quantity = models.IntegerField('数量', default=0)
    
    @property
    def order_amount(self):
        return self.item.price * self.order_quantity
