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
		]
	});
});

KindEditor.ready(function(K) {
        K.create('#text', {
                uploadJson : '../jsp/upload_json.jsp',
                fileManagerJson : '../jsp/file_manager_json.jsp',
                allowFileManager : true,
				imageUploadJson : '/',
        });
});

//KindEditor.ready(function(K) {
//	var str = K.unescape($("#editResult").text());
//	$("#editResult").html(str);
//});
