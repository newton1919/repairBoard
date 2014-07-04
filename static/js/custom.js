if ($('.summernote').length) {
      $('.summernote').summernote({
        height: 600,
        focus: true,
        toolbar: [['style', ['style']], ['style', ['bold', 'italic', 'underline', 'clear']], ['fontsize', ['fontsize']], ['color', ['color']], ['para', ['ul', 'ol', 'paragraph']], ['height', ['height']], ['insert', ['picture', 'link']], ['table', ['table']], ['fullscreen', ['fullscreen']]]
      });
}


$(function(){
	/*
	# =============================================================================
	#   DataTables
	# =============================================================================
	*/

	$("#dataTable1").dataTable({
	  "sPaginationType": "full_numbers",
	  aoColumnDefs: [
	    {
	      bSortable: false,
	      aTargets: [0, -1]
	    }
	  ]
	});
	$('.table').each(function() {
	  return $(".table #checkAll").click(function() {
	    if ($(".table #checkAll").is(":checked")) {
	      return $(".table input[type=checkbox]").each(function() {
	        return $(this).prop("checked", true);
	      });
	    } else {
	      return $(".table input[type=checkbox]").each(function() {
	        return $(this).prop("checked", false);
	      });
	    }
	  });
	});
	/*
    # =============================================================================
    #   File upload buttons
    # =============================================================================
    */

    $('.fileupload').fileupload();
    /*
    # =============================================================================
    #   Form wizard
    # =============================================================================
    */
    
    
    /*
    # =============================================================================
    #   company save
    # =============================================================================
    */
	$('#company').find(".btn-save").click(function(){
		var id = $(this).attr("id");
		var desc = $(".note-editable").html();
		$.post("/admin/company/"+id+"/update", { desc: desc },     
				function (data, textStatus){
					var ret = data.status;
					if (ret){
						location.href = "/admin/company/index";
					}else {
						alert("error");
					}
						
				},"json");
	});
	
	/* row action need confirm*/
	$('.confirm-message').hide();
	$('.row-actions').click(function(e){
		var need_confirm = $(this).attr("data-confirm");
		if (need_confirm == "True"){
			e.preventDefault();
			$('.confirm-message').fadeIn();
			$('.confirm-message').attr("data-href", $(this).attr("href"));
		}else{
			location.href = $(this).attr("href");
		}
	});
	$('.confirm-message').find('.btn-no').click(function(){
		$('.confirm-message').fadeOut();
	});
	$('.confirm-message').find('.btn-yes').click(function(){
		$('.confirm-message').fadeOut();
		location.href = $('.confirm-message').attr("data-href");
	});
	
	/* delete or edit appliance type*/
	$('.list-appliance-item > .icon-pencil').click(function(){
		alert("pencil");
	});
});