from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# index
def index(request):
    params = {
        "title": "",
        "sub_title": "",
    }
    return render(request, 'index.html', params)

# mainmenu
@login_required(login_url="/admin/login/")
def mainmenu(request):
    params = {
        "title": "管理メニュー",
        "sub_title": "管理メニュー",
    }
    return render(request, 'psys/MainMenu.html', params)


# @login_required(login_url="/admin/login/")
def customermanagementmenu(request):
    params = {
        "title": "管理メニュー",
        "sub_title": "得意先管理メニュー",
    }
    return render(request,'psys/CustomerManagementMenu.html', params)
