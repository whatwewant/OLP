from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from Forum.models import Post

def index(request):    
    return render(request, 'index.html', {})

def register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        nicename = request.POST.get("nicename")

        if not (len(username) >= 3 and len(username) <= 10):
            return render(request, "register.html", {"error": u"用户名只能是3-10个字符"})
        
        name = re.compile("^[_A-Za-z0-9]+$")
        if not name.match(username):
            return render(request, "register.html", {"error": u"用户名只能是数字和英文字符"})

        username_is_exist = User.objects.filter(username = username).exists()
        if username_is_exist:
            return render(request, "register.html", {"error": u"用户名已经存在"})
         
        if not(len(nicename) >= 2 and len(nicename) <= 10):
            return render(request, "register.html", {"error": u"昵称只能是2-10个字符"})

        mail = re.compile("[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$")
        if not mail.match(email):
            return render(request, "register.html", {"error": u"无效的邮箱格式"})

        if password != re_password:
            return render(request, "register.html", {"error": u"两次输入的密码不一致"})

        User.objects.create_user(username = username, password = password, email = email)
        UserProfile.objects.create_user(nicename = nicename)

        #return HttpResponseRedirect("/login/")
        return render(request, "register_success.html")
    
    before = requst.GET.get("before", "/")
    return render(request, "Account/register.html", {"before": before})



