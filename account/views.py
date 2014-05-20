
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect


def index(request):
   # return render(request, 'account/login.html')
    return HttpResponse("this is a login html")

'''
def login(request):
    if request.method == "POST": username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        

        if User.filter(pk=user.pk).exists():
            auth.login(request, user)
            next = request.POST.get("next", '/')
            #return HttpResponse(200)
            return render(request, 'accout/index.html')
            #return HttpResponseRedirect("/account/login")

        #return HttpResponse(500)
        login_failed_error=" login failed "
        return render(request, "account/login_failed.html", {"login_failed_error" : login_failed_error })

    next = request.GET.get("next", "/")
    return render(request, "account/login.html", {"next" : next })
'''

def login(request):
    if request.user.is_authenticated():
        return HttpReponse(u"you are already loggined")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None :
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/account/%d' % user.id)
        
            return HttpResponse(u'用户没有启用')
        
        return HttpResponse(u'用户名或密码错误')
    
    return render_to_response('account/login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('index.html')

