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
		
		if(id == ""){
			alert("请先保存。然后再上传图片。");
			return;
		}
		
		var sku_id = $(this).data("sku-id");
		//alert("sku_id:" + sku_id);
		if (sku_id != "undefined"){
			$("#album_trigger_sku_id").val(sku_id);
		}else{
			$("#album_trigger_sku_id").val("");
		}
		
		
		$("#file_upload_iframe").attr("src",'/admin/file-upload/' + type +'/' + id + '/');
		$("#picture_album_iframe").attr("src",'/admin/file-list/' + type +'/' + id + '/'); 
		$('.cd-popup').addClass('is-visible');
	});

	//close popup
	$('.cd-popup').on('click', function(event){
		if( $(event.target).is('.cd-popup-close') || $(event.target).is('.cd-popup') || $(event.target).is('.cd-popup-close-btn') ) {
			event.preventDefault();
			$(this).removeClass('is-visible');
		}
	});
	//close popup when clicking the esc keyboard button
	$(document).keyup(function(event){
		if(event.which=='27'){
			$('.cd-popup').removeClass('is-visible');
		}
	});
	
	$('#upload_picture_album a').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    })
});