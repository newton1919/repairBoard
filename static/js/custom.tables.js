custom_datatables = {
	validate_button: function () {
	    // Disable form button if checkbox are not checked
	    $("table").each(function (i) {
	      var checkboxes = $(this).find(":checkbox");
	      if(!checkboxes.length) {
	        // Do nothing if no checkboxes in this form
	        return;
	      }
	      if(!checkboxes.filter(":checked").length) {
	        $(this).parent().find(".table_actions.btn-danger").addClass("disabled");
	      }
	    });
	},
    disable_buttons: function() {
      $(".table_actions.disabled").click(function(event){
	    //event.preventDefault();
	    //event.stopPropagation();
	  });
	},
};

$(function(){
	custom_datatables.validate_button();
	custom_datatables.disable_buttons();
	// Change "select all" checkbox behaviour while any checkbox is checked/unchecked.
    $(".mainPanel").on("click", 'table tbody :checkbox', function (evt) {
      var $table = $(this).closest('table');
      var $multi_select_checkbox = $table.find('thead .multi_select_column');
      var any_unchecked = $table.find("tbody :checkbox").not(":checked");
      $multi_select_checkbox.prop('checked', !(any_unchecked.length > 0));
    });
    // Enable dangerous buttons only if one or more checkbox is checked.
    $("table").on("click", ':checkbox', function (evt) {
      var $table = $(this).closest("table");
      var any_checked = $table.find("tbody :checkbox").is(":checked");
      if(any_checked) {
    	  $(".table_actions.btn-danger").removeClass("disabled");
      }else {
    	  $(".table_actions.btn-danger").addClass("disabled");
      }
    });
    //$(".table_actions.btn-danger")取消默认操作，变成批量操作
    $(".table_actions.btn-danger").click(function(event){
    	event.preventDefault();
    	var action_url = $(this).attr('href');
    	var checked = $('table').find("tbody :checkbox:checked");
    	var delete_list = [];
    	checked.each(function(index){
    		delete_list.push($(this).val());
    	});
    	var data = {"delete_list": JSON.stringify(delete_list)};
    	$.post(action_url, data, function(data2, textStatus){
    		var ret = data2.status;
			if (ret){
				location.reload();
			}else {
				alert(data2.message);
				location.reload();
			}
    	}, 'json');
    });
});