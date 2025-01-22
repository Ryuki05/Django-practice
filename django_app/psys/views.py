from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import EmployeeRegistrationForm, CustomerForm, OrderForm, OrderDetailFormSet, ItemForm
from .models import Customer, Orders, OrderDetails, Item, Employee
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm


class SignUpView(generic.CreateView):
    form_class = EmployeeRegistrationForm
    template_name = 'psys/signup.html'
    success_url = reverse_lazy('psys:login')

    def form_valid(self, form):
        # パスワードをハッシュ化して保存
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'サインアップが完了しました。ログインしてください。')
        return super().form_valid(form)


class LoginView(View):
    template_name = 'psys/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('psys:main_menu')
        return render(request, self.template_name)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('psys:main_menu')
            else:
                messages.error(request, '従業員番号またはパスワードが間違っています。')
        return render(request, self.template_name, {'form': form})

class RegisterView(generic.CreateView):
    form_class = EmployeeRegistrationForm
    template_name = 'psys/register.html'
    success_url = reverse_lazy('psys:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'登録が完了しました。従業員番号は {self.object.employee_number} です。')
        return response

class MainMenuView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'psys/main_menu.html'
    login_url = 'psys:login'

class CustomerListView(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'psys/customer_list.html'
    context_object_name = 'customers'
    login_url = 'psys:login'

    def get_queryset(self):
        return Customer.objects.filter(delete_flag=False).order_by('customer_code')

class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Customer
    template_name = 'psys/customer_detail.html'
    context_object_name = 'customer'
    slug_field = 'customer_code'
    slug_url_kwarg = 'customer_code'
    login_url = 'psys:login'

class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Customer
    template_name = 'psys/customer_form.html'
    fields = ['customer_code', 'customer_name', 'customer_telno', 'customer_address']
    success_url = reverse_lazy('psys:customer_list')
    login_url = 'psys:login'

    def form_valid(self, form):
        messages.success(self.request, '得意先を登録しました。')
        return super().form_valid(form)

class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    template_name = 'psys/customer_form.html'
    fields = ['customer_name', 'customer_telno', 'customer_address']
    slug_field = 'customer_code'
    slug_url_kwarg = 'customer_code'
    login_url = 'psys:login'

    def get_success_url(self):
        return reverse_lazy('psys:customer_detail', kwargs={'customer_code': self.object.customer_code})

    def form_valid(self, form):
        messages.success(self.request, '得意先情報を更新しました。')
        return super().form_valid(form)

class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Customer
    template_name = 'psys/customer_confirm_delete.html'
    success_url = reverse_lazy('psys:customer_list')
    slug_field = 'customer_code'
    slug_url_kwarg = 'customer_code'
    login_url = 'psys:login'

    def delete(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete_flag = True
        customer.save()
        messages.success(request, '得意先を削除しました。')
        return redirect(self.success_url)

class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Orders
    template_name = 'psys/order_list.html'
    context_object_name = 'orders'
    login_url = 'psys:login'

    def get_queryset(self):
        return Orders.objects.filter(delete_flag=False).order_by('order_number')

class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Orders
    template_name = 'psys/order_detail.html'
    context_object_name = 'order'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'
    login_url = 'psys:login'

class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Orders
    form_class = OrderForm
    template_name = 'psys/order_form.html'
    success_url = reverse_lazy('psys:order_list')
    login_url = 'psys:login'

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

class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Orders
    form_class = OrderForm
    template_name = 'psys/order_form.html'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'
    login_url = 'psys:login'

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

class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Orders
    template_name = 'psys/order_confirm_delete.html'
    success_url = reverse_lazy('psys:order_list')
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'
    login_url = 'psys:login'

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        order.delete_flag = True
        order.save()
        messages.success(request, '受注を削除しました。')
        return redirect(self.success_url)

class ItemListView(LoginRequiredMixin, generic.ListView):
    model = Item
    template_name = 'psys/item_list.html'
    context_object_name = 'items'
    login_url = 'psys:login'

    def get_queryset(self):
        return Item.objects.filter(delete_flag=False).order_by('item_code')

class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = Item
    template_name = 'psys/item_detail.html'
    context_object_name = 'item'
    slug_field = 'item_code'
    slug_url_kwarg = 'item_code'
    login_url = 'psys:login'

class ItemCreateView(LoginRequiredMixin, generic.CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'psys/item_form.html'
    success_url = reverse_lazy('psys:item_list')
    login_url = 'psys:login'

    def form_valid(self, form):
        messages.success(self.request, '商品を登録しました。')
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'psys/item_form.html'
    slug_field = 'item_code'
    slug_url_kwarg = 'item_code'
    login_url = 'psys:login'

    def get_success_url(self):
        return reverse_lazy('psys:item_detail', kwargs={'item_code': self.object.item_code})

    def form_valid(self, form):
        messages.success(self.request, '商品情報を更新しました。')
        return super().form_valid(form)

class ItemDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Item
    template_name = 'psys/item_confirm_delete.html'
    success_url = reverse_lazy('psys:item_list')
    slug_field = 'item_code'
    slug_url_kwarg = 'item_code'
    login_url = 'psys:login'

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete_flag = True
        item.save()
        messages.success(request, '商品を削除しました。')
        return redirect(self.success_url)

@login_required(login_url='psys:login')
def employee_create(request):
    if request.method == 'POST':
        try:
            # POSTデータの取得（getメソッドを使用）
            employee_no = request.POST.get('employee_no')
            employee_name = request.POST.get('employee_name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            # 必要なデータが存在するかチェック
            if not all([employee_no, employee_name, email, password]):
                messages.error(request, '全てのフィールドを入力してください。')
                return render(request, 'psys/employee_create.html')

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