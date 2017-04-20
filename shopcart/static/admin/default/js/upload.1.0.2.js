$(function(){
	/*modal 下拉选择*/
	$("#selectOption li").click(function(obj){
		var option=$(this).text();
		$(".selectInput").text(option);
	});
})
jQuery(document).ready(function($){
	//open popup
	$('.cd-popup-trigger').on('click', function(event){
		event.preventDefault();
		type = $(this).data("type");
		id = $(this).data("id");
		
		which_page = $(this).data("which-page");
		console.log("which-page:" + which_page);
		if (which_page=="" || which_page==undefined){
			which_page = 'NotSet';
		}else{
			which_page = "popup-content-" + which_page;
		}
		
		console.log('which_page:' + which_page);
		
		if(id == ""){
			alert("请先保存。然后再上传图片。");
			return;
		}
		
		
		$("#open_file_upload_trigger").val($(this).data('trigger-name'));
		
		var sku_id = $(this).data("sku-id");
		//alert("sku_id:" + sku_id);
		if (sku_id != undefined){
			$("#album_trigger_sku_id").val(sku_id);
		}else{
			$("#album_trigger_sku_id").val("");
		}
		
		var extra_info = $(this).data("extra-info");
		console.log('pop extra-info:' + extra_info);
		var extraurl = "";
		if (extra_info!=undefined){
			extraurl = "?extra-info=" + extra_info;
		}
		
		$("#file_upload_iframe").attr("src",'/admin/file-upload/' + type +'/' + id + '/' + extraurl);
		$("#picture_album_iframe").attr("src",'/admin/file-list/' + type +'/' + id + '/'); 
		
		if (which_page != 'NotSet'){
			tab_name = "#upload_picture_album a[href='#" + which_page +"']";
			console.log('tab_name:' + tab_name);
			$(tab_name).tab('show');
		}
		
		
		$('.cd-popup.album-modal-win').addClass('is-visible');
	});
	
	$('#upload_picture_album a').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    })
});