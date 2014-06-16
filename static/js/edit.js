/* Use KindEditor */

KindEditor.ready(function(K) {
	window.editor = K.create("#content", {
		themeType : 'default',
		items : [
			'code', 'source',
			'undo', 'redo',
			'link', 'unlink',
			'justifyleft', 'justifycenter', 'justifyright',
			'hr', 'fontsize',  'fontname',
			'italic', 'bold',
			'image',
            'media',
		]
	});
});

/*
KindEditor.ready(function(K) {
        K.create('#text', {
                uploadJson : '../jsp/upload_json.jsp',
                fileManagerJson : '../jsp/file_manager_json.jsp',
                allowFileManager : true,
				imageUploadJson : '/',
        });
});*/

//KindEditor.ready(function(K) {
//	var str = K.unescape($("#editResult").text());
//	$("#editResult").html(str);
//});
/*
$(document).ready(function() {
	$("form").submit(function (e) {
		var title 	= $("#title").val();
			content	= $("#content").val();
			excerpt	= $("#excerpt").val();
			// content_type = $("#content_type").val();
		if(!title || !content || !excerpt) {
			e.preventDefault();
			$(".error").css("color", "red");
			if(!title)
				$("span").show();
		}
	});
});

$(document).ready(function() {
	$("#title").change(function() {
		$("span").hide();
	});
});
*/
