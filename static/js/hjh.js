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
