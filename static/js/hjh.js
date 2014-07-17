
/* If tag doesnot exist, alert*/
function exist ( e ){
    if($(e).length <= 0) {
        alert(e + "不存在,请检查标签");
        return false;
    }
    return true;
} 

/* if tag value is empty, alert*/
function empty (e, des) {
    if($(e).val() == '') {
        alert(des + '不能为空');
        // $(e).preventDefault();
        return true;
    }
    return false;
}

/* daytime / night mode
*/
$(document).ready(function () {
    $(".nightmode").click(function () {
        $(".daytime,pre,p,h1,h2,h3,h4,h5,h6").css("background-color", "#484848");
    });
});

$(document).ready(function () {
    $(".daytimemode").click(function () {
        $(".daytime,pre,p,h1,h2,h3,h4,h5,h6").css("background-color", "#FFF");
    });
});

$(document).ready(function () {
    $(".data-delete").click(function (e) {
        if (confirm("确定要删除吗?")) {
            e.submit();
        } else {
            e.preventDefault();
        }
    });
});

/*
$(document).ready(function () {
    $(".password-submit").click(function () {
        $(".password-input").val($.md5($(".password-input").val()));
        if($(".dopassword-input").length > 0) {
            $(".dopassword-input").val($.md5($(".dopassword-input").val()));
        }
    });
}); */

function calcMD5() {
    $(".password-input").val($.md5($(".password-input").val()));
    if($(".dopassword-input").length > 0) {
        $(".dopassword-input").val($.md5($(".dopassword-input").val()));
    }
}

$(document).ready(function () {
    $(".password-submit").click(function (e) {
        if(empty(".username", '用户名') || empty(".password-input", '密码') || empty(".dopassword-input", '确认密码')) {
            e.preventDefault();
            //return false;
        }
        calcMD5();
        e.submit();
        //return true;
    });
});