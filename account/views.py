'''view'''

#coding=utf-8


# check if the user exist
from django.contrib.auth.models import User

# use it to a httpresponse
import json


# json httpResponse
#def message(status, content):
#    response_json = {"status": status, "content": content}
#    return HttpResponse(json.dumps(response_json))


def user_exist(username):
    try:
        User.objects.get(username=username)
    except User.DoseNotExist:
        return False
    return True

def login(request):
    if request.method == "POST":
        username = request.POST.get("username","-1")
        password = request.POST.get("password","-1")
        user = auth.authenticate(username=username, password=password)
        
        if user is not None and user.is_active:
            auth.logout(request)
            auth.login(request, user)
            next = request.POST.get("next","/")
            # json httpResponse
            response_json = {"status" :"success", "redirect" :next}
            return HttpResponse(json.dumps(response_json))
        else:
            response_json = {"status": "error", "content" :u"用户名或密码错误"}
            return HttpResponse(json.dumps(response_json))
    else:
        next = request.GET.get("next","/")
        return render(request,"account/login.html",{"next" :next })



