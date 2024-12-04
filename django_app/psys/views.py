from django.shortcuts import render
from django.contri.auth.decorators import login_required
from django.contrib.auth.models import User
#index
def index(request):

    params = {
        "title": "",
        "sub_title": "",
    }

    return render(request,'index.html',params)
#mainmenu
@login_required(login_url = "admin/login/")
def mainmenu(reqest):
    params = {
        "title": "管理メニュー",
        "sub_title": "管理メニュー",
    }


    return render(request, 'psys/MainMenu.html',params)