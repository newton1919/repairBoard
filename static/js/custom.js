if ($('#summernote').length) {
      $('#summernote').summernote({
        height: 600,
        focus: true,
        toolbar: [['style', ['style']], ['style', ['bold', 'italic', 'underline', 'clear']], ['fontsize', ['fontsize']], ['color', ['color']], ['para', ['ul', 'ol', 'paragraph']], ['height', ['height']], ['insert', ['picture', 'link']], ['table', ['table']], ['fullscreen', ['fullscreen']]]
      });
}

$(function(){
	$(".btn-save").click(function(){
		var desc = $(".note-editable").html();
		$.post("/admin/company/saiway/update", { desc: desc },     
				function (data, textStatus){
					var ret = data.status;
					if (ret){
						location.href = "/admin/index";
					}else {
						alert("error");
					}
						
				},"json");
	});

});