from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from .forms import LoginForm, EmployeeRegistrationForm, CustomerForm, OrderForm, OrderDetailFormSet, ItemForm
from .models import Customer, Orders, OrderDetails, Item, Employee
from django.db import transaction
from django.contrib.auth.hashers import make_password

class CustomLoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'psys/login.html'
    success_url = reverse_lazy('psys:main_menu')

    def form_valid(self, form):
        employee_number = form.cleaned_data.get('employee_number')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, employee_number=employee_number, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'ログインしました。')
            return super().form_valid(form)
        else:
            messages.error(self.request, '従業員番号またはパスワードが正しくありません。')
            return self.form_invalid(form)

class RegisterView(generic.CreateView):
    form_class = EmployeeRegistrationForm
    template_name = 'psys/register.html'
    success_url = reverse_lazy('psys:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'登録が完了しました。従業員番号は {self.object.employee_number} です。')
        return response

class MainMenuView(generic.TemplateView):
    template_name = 'psys/main_menu.html'

class CustomerListView(generic.ListView):
    model = Customer
    template_name = 'psys/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.filter(delete_flag=False).order_by('customer_code')

class CustomerDetailView(generic.DetailView):
    model = Customer
    template_name = 'psys/customer_detail.html'
    context_object_name = 'customer'
    slug_field = 'customer_code'
    slug_url_kwarg = 'customer_code'

class CustomerCreateView(generic.CreateView):
    model = Customer
    template_name = 'psys/customer_form.html'
    fields = ['customer_code', 'customer_name', 'customer_telno', 'customer_address']
    success_url = reverse_lazy('psys:customer_list')

    def form_valid(self, form):
        messages.success(self.request, '得意先を登録しました。')
        return super().form_valid(form)

class CustomerUpdateView(generic.UpdateView):
    model = Customer
    template_name = 'psys/customer_form.html'
    fields = ['customer_name', 'customer_telno', 'customer_address']
    slug_field = 'customer_code'
    slug_url_kwarg = 'customer_code'

    def get_success_url(self):
        return reverse_lazy('psys:customer_detail', kwargs={'customer_code': self.object.customer_code})

    def form_valid(self, form):
        messages.success(self.request, '得意先情報を更新しました。')
        return super().form_valid(form)

class CustomerDeleteView(generic.DeleteView):
    model = Customer
    template_name = 'psys/customer_confirm_delete.html'
    success_url = reverse_lazy('psys:customer_list')
    slug_field = 'customer_code'
    slug_url_kwarg = 'customer_code'

    def delete(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete_flag = True
        customer.save()
        messages.success(request, '得意先を削除しました。')
        return redirect(self.success_url)

class OrderListView(generic.ListView):
    model = Orders
    template_name = 'psys/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Orders.objects.filter(delete_flag=False).order_by('order_number')

class OrderDetailView(generic.DetailView):
    model = Orders
    template_name = 'psys/order_detail.html'
    context_object_name = 'order'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'

class OrderCreateView(generic.CreateView):
    model = Orders
    form_class = OrderForm
    template_name = 'psys/order_form.html'
    success_url = reverse_lazy('psys:order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['details'] = OrderDetailFormSet(self.request.POST)
        else:
            context['details'] = OrderDetailFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        details = context['details']
        with transaction.atomic():
            self.object = form.save()
            if details.is_valid():
                details.instance = self.object
                details.save()
                messages.success(self.request, '受注を登録しました。')
                return super().form_valid(form)
        return self.form_invalid(form)

class OrderUpdateView(generic.UpdateView):
    model = Orders
    form_class = OrderForm
    template_name = 'psys/order_form.html'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['details'] = OrderDetailFormSet(self.request.POST, instance=self.object)
        else:
            context['details'] = OrderDetailFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        details = context['details']
        with transaction.atomic():
            self.object = form.save()
            if details.is_valid():
                details.instance = self.object
                details.save()
                messages.success(self.request, '受注情報を更新しました。')
                return super().form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('psys:order_detail', kwargs={'order_number': self.object.order_number})

class OrderDeleteView(generic.DeleteView):
    model = Orders
    template_name = 'psys/order_confirm_delete.html'
    success_url = reverse_lazy('psys:order_list')
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        order.delete_flag = True
        order.save()
        messages.success(request, '受注を削除しました。')
        return redirect(self.success_url)

class ItemListView(generic.ListView):
    model = Item
    template_name = 'psys/item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.filter(delete_flag=False).order_by('item_code')

class ItemDetailView(generic.DetailView):
    model = Item
    template_name = 'psys/item_detail.html'
    context_object_name = 'item'
    slug_field = 'item_code'
    slug_url_kwarg = 'item_code'

class ItemCreateView(generic.CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'psys/item_form.html'
    success_url = reverse_lazy('psys:item_list')

    def form_valid(self, form):
        messages.success(self.request, '商品を登録しました。')
        return super().form_valid(form)

class ItemUpdateView(generic.UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'psys/item_form.html'
    slug_field = 'item_code'
    slug_url_kwarg = 'item_code'

    def get_success_url(self):
        return reverse_lazy('psys:item_detail', kwargs={'item_code': self.object.item_code})

    def form_valid(self, form):
        messages.success(self.request, '商品情報を更新しました。')
        return super().form_valid(form)

class ItemDeleteView(generic.DeleteView):
    model = Item
    template_name = 'psys/item_confirm_delete.html'
    success_url = reverse_lazy('psys:item_list')
    slug_field = 'item_code'
    slug_url_kwarg = 'item_code'

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete_flag = True
        item.save()
        messages.success(request, '商品を削除しました。')
        return redirect(self.success_url)

def employee_create(request):
    if request.method == 'POST':
        try:
            # POSTデータの取得
            employee_no = request.POST['employee_no']
            employee_name = request.POST['employee_name']
            email = request.POST['email']
            password = request.POST['password']

            # 従業員番号の重複チェック
            if Employee.objects.filter(employee_no=employee_no).exists():
                messages.error(request, '指定された従業員番号は既に使用されています。')
                return render(request, 'psys/employee_create.html')

            # メールアドレスの重複チェック
            if Employee.objects.filter(email=email).exists():
                messages.error(request, '指定されたメールアドレスは既に使用されています。')
                return render(request, 'psys/employee_create.html')

            # 新規従業員の作成
            employee = Employee.objects.create(
                employee_no=employee_no,
                employee_name=employee_name,
                email=email,
                password=make_password(password),  # パスワードをハッシュ化
                is_active=True
            )
            
            messages.success(request, '従業員登録が完了しました。')
            return redirect('psys:main_menu')

        except Exception as e:
            messages.error(request, f'登録中にエラーが発生しました: {str(e)}')
            return render(request, 'psys/employee_create.html')

    return render(request, 'psys/employee_create.html')
