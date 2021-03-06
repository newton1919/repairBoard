if ($('.summernote').length) {
      $('.summernote').summernote({
        height: 600,
        focus: true,
        toolbar: [['style', ['style']], ['style', ['bold', 'italic', 'underline', 'clear']], ['fontsize', ['fontsize']], ['color', ['color']], ['para', ['ul', 'ol', 'paragraph']], ['height', ['height']], ['insert', ['picture', 'link']], ['table', ['table']], ['fullscreen', ['fullscreen']]]
      });
}


$(function(){
	/*navbar active*/
//	$('.navbar-nav > li').click(function(e) {
//	    $('.navbar-nav > li.active').removeClass('active');
//	    var $this = $(this);
//	    if (!$this.hasClass('active')) {
//	        $this.addClass('active');
//	    }
//	    
//	});
	/*设置语言*/
	$(".btn.language").click(function(){
		var lang = $(this).attr("data-language");
		$.get("/language",{"language":lang}, 
			function (data, textStatus){
				var ret = data.status;
				if (ret){
					location.reload();
				}else {
					alert(data.message);
					location.reload();
				}
			},"json");
	});
	
	/*确保modal不是只load一次远程内容，每次都清空重新load */
	$(document).on("hidden.bs.modal", function (e) { $(e.target).removeData("bs.modal").find(".modal-content").empty(); });
	
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
	
	/* row action need confirm*/
	//$('.confirm-message').hide();
	$('.row-actions').click(function(e){
		var need_confirm = $(this).attr("data-confirm");
		var modal = $(this).attr("data-toggle");
		if (need_confirm == "True"){
			e.preventDefault();
			$('.confirm-message').fadeIn();
			$('.confirm-message').attr("data-href", $(this).attr("href"));
		}else if(modal == "modal"){
			
		}else {
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
	
	/* delete appliance type*/
	//$('.confirm-type-message').hide();
	$('.list-appliance-item > .icon-trash').click(function(e){
		e.preventDefault();
		var type_id = $(this).parent().attr("data-ref");
		$('.confirm-type-message').fadeIn();
		$('.confirm-type-message').attr("data-href", "/admin/appliance_type/"+type_id+"/delete");
		e.stopPropagation();
	});
	$('.confirm-type-message').find('.btn-no').click(function(){
		$('.confirm-type-message').fadeOut();
	});
	$('.confirm-type-message').find('.btn-yes').click(function(){
		$('.confirm-type-message').fadeOut();
		location.href = $('.confirm-type-message').attr("data-href");
	});
});