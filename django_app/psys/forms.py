from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Employee, Customer, Orders, OrderDetails, Item

class EmployeeRegistrationForm(forms.ModelForm):
    employee_no = forms.CharField(label='従業員番号', max_length=8)
    name = forms.CharField(label='名前', max_length=100)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ('employee_number', 'name', 'password')

    def clean_employee_no(self):
        employee_number = self.cleaned_data['employee_no']
        if Employee.objects.filter(employee_number=employee_number).exists():
            raise forms.ValidationError('この従業員番号は既に使用されています。')
        return employee_number


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'customer_telno', 'customer_postalcode', 
                 'customer_address', 'discount_rate']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_telno': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_postalcode': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_address': forms.TextInput(attrs={'class': 'form-control'}),
            'discount_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'customer_name': '得意先名',
            'customer_telno': '電話番号',
            'customer_postalcode': '郵便番号',
            'customer_address': '住所',
            'discount_rate': '割引率',
        } 

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['order_number', 'customer', 'order_date', 'delivery_date']
        widgets = {
            'order_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'delivery_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'order_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'customer': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean_order_number(self):
        order_number = self.cleaned_data['order_number']
        if self.instance.pk is None:  # 新規登録の場合のみ重複チェック
            if Orders.objects.filter(order_number=order_number).exists():
                raise forms.ValidationError('この受注番号は既に使用されています。')
        return order_number

class OrderDetailFormSet(forms.models.inlineformset_factory(
    Orders, OrderDetails,
    fields=['item', 'order_quantity'],
    extra=1,
    can_delete=True,
    widgets={
        'item': forms.Select(attrs={'class': 'form-control'}),
        'order_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
    }
)):
    def clean(self):
        super().clean()
        if not any(form.cleaned_data and not form.cleaned_data.get('DELETE', False)
                  for form in self.forms):
            raise forms.ValidationError('少なくとも1つの商品を登録してください。') 

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_code', 'item_name', 'price', 'stock_quantity']
        widgets = {
            'item_code': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'placeholder': '商品コードを入力'
            }),
            'item_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'placeholder': '商品名を入力'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'min': '0'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'min': '0'
            })
        }

    def clean_item_code(self):
        item_code = self.cleaned_data['item_code']
        if self.instance.pk is None:  # 新規登録の場合のみ重複チェック
            if Item.objects.filter(item_code=item_code).exists():
                raise forms.ValidationError('この商品コードは既に使用されています。')
        return item_code 