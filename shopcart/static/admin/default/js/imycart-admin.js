jQuery(document).ready(function() {
    "use strict";
	// Django需要验证csrf信息验证提交人身份，这段代码必须，需要放入公共JS
	// csrf信息开始
		function getCookie(name) {
			var cookieValue = null;
			if (document.cookie && document.cookie != '') {
				var cookies = document.cookie.split(';');
				for (var i = 0; i < cookies.length; i++) {
					var cookie = jQuery.trim(cookies[i]);
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) == (name + '=')) {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break;
					}
				}
			}
			return cookieValue;
		}
		var csrftoken = getCookie('csrftoken');
	
		function csrfSafeMethod(method) {
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			}
		});
		// csrf信息结束
});


/***
	Common functions
***/
$(function(){
    $.ajaxSetup ({
        cache: false //关闭AJAX缓存
    });
});

//公共的调用ajax方法
function imycartAjaxCall(url,object,is_show_message_box,message){
	var encodedata = $.toJSON(object);
	$.ajax({
			type : 'POST',
			contentType : 'application/json',
			dataType : 'json',
			url : url,
			data : encodedata,
			success : function(result) {
				if(result.success==true){
					if(is_show_message_box){
						if(message==null){
							message = "Your opration is success.";
						}else if(message=='showservermessage'){
								message = result.message;
						}
						$("#infoMessage").html(message);
					}
				}else{
					if(message==null){
							message = "Your opration is failed.";
					}else if(message=='showservermessage'){
							message = result.message;
					}
					$("#infoMessage").html(message);
				}
				$("#myModal").modal('toggle');
			},
			error : function(result) {
				alert(result.success);
			}
	});
};
//带回调函数的ajax请求通用方法
function imycartAjaxCallWithCallback(url,object,callback,triggerControl,extraInfo){
	var encodedata = $.toJSON(object);
	$.ajax({
			type : 'POST',
			contentType : 'application/json',
			dataType : 'json',
			url : url,
			data : encodedata,
			success : function(result) {
				callback(result,triggerControl,extraInfo);
			},
			error : function(result) {
				alert(result.success);
			}
	});
};

//公共方法

//下拉菜单选项切换
jQuery(".dropdown-item").click(function(){
	var select_text = $(this).text();	
	var value = $(this).data("value");
	$(this).parent().parent().find(".inputBtn").find(".selected-text").text(select_text);
	$(this).parent().parent().find(".dropdown-item-input").val(value); // 将选中的值放入隐藏的input
});


jQuery(".dropdown-item-sku-img").click(function(){
	var value = $(this).data("value");
	var select_text = $(this).data("select-text");
	$(this).parent().parent().find(".inputBtn").find(".selected-text").text(select_text);
	$(this).parent().parent().find(".dropdown-item-input").val(value); // 将选中的值放入隐藏的input	
	
	var sku_id = $(this).data("sku-id");
	var thumb = $(this).find(".sku-thumb").attr("src");
	$("#sku_img_" + sku_id).attr("src",thumb);
});

//全选复选框选择
jQuery("#main-content-checkbox-all").change(function(){
	if($("#main-content-checkbox-all").is(":checked")){
		//从没选中到选中
		$("#main-content-table").find("input[type='checkbox']").each(function(){
			$(this).prop("checked", true);//jQuery1.6以上，都要使用prop属性，不然会出现只能选中一次，第二次无效的问题。
		});
	}else{
		$("#main-content-table").find("input[type='checkbox']").each(function(){
			$(this).prop("checked", false);
		});
	}
}); 

jQuery("#main-content-btn-all").click(function(e){
	event.preventDefault();
	if($("#main-content-checkbox-all").is(":checked")){
		$("#main-content-checkbox-all").prop("checked",false);
	}else{
		$("#main-content-checkbox-all").prop("checked",true);
	}
	$("#main-content-checkbox-all").trigger("change");
});


//页码切换
//页数点击切换
jQuery(".pageChage").click(function(){
	event.preventDefault();//阻止A标签跳转
	var url = location.href;
	var pageNo = $.getUrlParam("page");
	var tag = $(this).attr("data-tag");
	if(tag=="Previous"){
		//向前，如果当前不是第一页，则向前翻页
		if(pageNo>1){
			pageNo--;
			var newurl = changeURLArg(url,"page",pageNo);
			location.href = newurl;//跳转到对应的页面
		}
	}else if(tag=="Next"){
		//向后，如果当前不是最后一页，则翻页
		var pages = $(this).data("page-range");
		if(pageNo<pages){
			pageNo++;
			var newurl = changeURLArg(url,"page",pageNo);
			location.href = newurl;//跳转到对应的页面
		}
	}else{
			var page = $(this).data("page");
			var newurl = changeURLArg(url,"page",page);
			location.href = newurl;//跳转到对应的页面
	}
});



//订单管理界面
jQuery("#order_batch_delete").click(function(e){
	var id_list = [];
	 $("input[name='is_oper']").each(function(){
		if($(this).is(':checked')){
			id_list.push($(this).data("order-id"));
		}
	});
	var oper_ids = id_list.join(',');
	$("#oper-ids").val(oper_ids);
	$("#order_oper_form").submit();
});

//订单备注添加
jQuery("#order-remark-add-submit-btn").click(function(){
	var url = "/admin/order-remark-add/";

	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#order-remark-add-form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			$('#myModal').on('hidden.bs.modal', function (e) {
				var url = location.href;
				var newurl = changeURLArg(url,"tab_name","tag4");
				location.href = newurl;//跳转到对应的页面
			});
			
			$("#myModal").modal('toggle');
			
		}
	});
});

//订单详情tab页切换
$(".tag li").on("click", function () {
    var contentId = $(this).attr("data");
    $(".tag li,.add-content").removeClass("active");
    $(this).addClass("active");
    $("#" + contentId).addClass("active");
})


//商品管理界面
//Tab页切换方法
//添加商品，页签（基本信息-属性-相册）点击事件
$(".product-info-tag li").on("click",function(){
	if($("input[name=id]").val()!=''){
		var contentId=$(this).attr("data");
		$(".product-info-tag li,.add-content").removeClass("active");
		$(this).addClass("active");
		$("#"+contentId).addClass("active");
	}else{
		$("#infoMessage").html("请先保存商品基本信息。");
		$("#myModal").modal('toggle');
	}
});

//商品分类选择
jQuery(".category-selection-checkbox").click(function(){
	var category_id_list = new Array();
	$("#product_category_selection").find("input[type='checkbox']").each(function(){
		if ($(this).prop("checked")){
			category_id_list.push($(this).data("cat-id"));
		}
	});
	$("input[name='product_category_list']").val(category_id_list.join(","));
});

//生成SKU页面，选择某个分类后的处理
jQuery(".add-attribute-group").click(function(){
	var selected_group_id = $("input[name=attribute-group]").val();
	
	//判断是否已经选择了属性组
	if (selected_group_id.trim()==""){
		$("#infoMessage").html("请选择一个属性组");
		$("#myModal").modal('toggle');
		return;
	}
	//判断选择的属性组是否已经在界面上了
	var terget_id = "group_div_parent_" + selected_group_id;
	if( $("#" + terget_id).size() ){
		$("#infoMessage").html("属性组已经添加了");
		$("#myModal").modal('toggle');
		return;
	}else{
		// 不存在
		var url = "/attribute/group/info/" + selected_group_id + "/";
		$.ajax({
			cache: false,
			type: "POST",
			url:url,
			data:null,
			async: false,
			error: function(request) {
				alert("System error");
			},
			success: function(data) {
				
				var $pdiv = $("<div>",{
					id:'group_div_parent_' + selected_group_id,
					//text:'this is a test',
					"class":"item-free attr-array",
					}).appendTo($("#attribute_group_show"));
				
				var $title = $("<div>",{
					id:'title_div_' + selected_group_id,
					text:"删除 | " + data.data.group.name + " - " + data.data.group.code,
					"class":"attr-array-title",
					}).appendTo($pdiv);
				
				var $item = $("<div>",{
					id:'items_' + selected_group_id,
					//text:'Color 组',
					"class":"attr-array-item",
					}).appendTo($pdiv);
				
				//为了排序，先整理成数组
				var itemArray = new Array();
				$.each(data.data.items,function(index,attr){
					itemArray.push(attr);
				});
				itemArray.sort();
				
				$.each(itemArray,function(index,attr){
					$('<input type="checkbox" value="'+ attr.id +'" name="attribute-id" class="attribute-to-sku" data-attr-id="' + attr.id + '" /><label>' + attr.name + '</label>').appendTo($item);
				});
			}
		});
	} 
});

//生成SKU按钮
jQuery(".make-sku-list").click(function(){
	var product_id = $("input[name=id]").val();
	var url = "/admin/product-sku-manage/" + product_id + "/";

	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#arrtibute_to_make_sku").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			$('#myModal').on('hidden.bs.modal', function (e) {
				var url = location.href;
				var newurl = changeURLArg(url,"tab_name","tag_attribute");
				location.href = newurl;//跳转到对应的页面
			});
			
			$("#myModal").modal('toggle');
			
		}
	});
});

//保存SKU属性
jQuery("#product-attribute-submit-btn").click(function(){
	var url = "/admin/product-sku-attribute-manage/";

	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#sku_attribute_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			$('#myModal').on('hidden.bs.modal', function (e) {
				var url = location.href;
				var newurl = changeURLArg(url,"tab_name","tag_attribute");
				location.href = newurl;//跳转到对应的页面
			});
			
			$("#myModal").modal('toggle');
			
		}
	});
	
});

//删除SKU
jQuery(".sku_delete_link").click(function(){
	event.preventDefault();//阻止A标签跳转
	
	var url = "/admin/product-sku-delete/" + $(this).data("sku-id") + "/";

	$.ajax({
		cache: false,
		type: "GET",
		url:url,
		data:null,
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			$('#myModal').on('hidden.bs.modal', function (e) {
				var url = location.href;
				var newurl = changeURLArg(url,"tab_name","tag_attribute");
				location.href = newurl;//跳转到对应的页面
			});
			
			$("#myModal").modal('toggle');
			
		}
	});
});


//商品图片管理

//设为主图
jQuery(".set-to-main-picture-link").click(function(){
	event.preventDefault();
	var img_url = $(this).data("image-url");
	$("input[name=product_image]").val(img_url);
	$("#product_main_image").attr("src",img_url);
});

//保存主图设置和SKU图设置
jQuery("#product-picture-manage-submit-btn").click(function(){
	var url = "/admin/product-picture-manage/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#product_picture_manage_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				//$('#myModal').on('hidden.bs.modal', function (e) {
				//	location.href = url + "?id=" + data.data.product_id;
				//})
			}
			$("#myModal").modal('toggle');
		}
	});
	
});



jQuery("#product-batch-delete").click(function(e){
	var id_list = [];
	 $("input[name='is_oper']").each(function(){
		if($(this).is(':checked')){
			id_list.push($(this).data("order-id"));
		}
	});
	var oper_ids = id_list.join(',');
	$("#oper-ids").val(oper_ids);
	$("#oper-method").val('delete');
	$("#product_oper_form").submit();
});

jQuery(".product-batch-publish").click(function(e){
	var id_list = [];
	 $("input[name='is_oper']").each(function(){
		if($(this).is(':checked')){
			id_list.push($(this).data("order-id"));
		}
	});
	var oper_ids = id_list.join(',');
	$("#oper-ids").val(oper_ids);
	if($(this).data("method")=="on"){
		$("#oper-method").val('onpublish');
	}else{
		$("#oper-method").val('offpublish');
	}
	
	$("#product_oper_form").submit();
});


jQuery("#product-basic-info-submit-btn").click(function(e){
	var url = "/admin/product-edit/";
	//由于使用了ckeditor，直接获取文本域的值，会丢失修改部分的信息，因此要先用api获取修改以后的值填到文本域中
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#product-basic-info-form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.href = url + "?id=" + data.data.product_id;
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});



jQuery("#product-detail-info-submit-btn").click(function(e){
	var url = "/admin/product-detail-manage/";
	//由于使用了ckeditor，直接获取文本域的值，会丢失修改部分的信息，因此要先用api获取修改以后的值填到文本域中
	
	var data = CKEDITOR.instances.product_desc_editor.getData();
	$("#product_desc_editor").val(data);
	//alert($("#editor").val())
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#product-detail-info-form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			$("#myModal").modal('toggle');
			if(data.success==true){
				;
			}
		}
	});
});




//通用函数
/* 
* url 目标url 
* arg 需要替换的参数名称 
* arg_val 替换后的参数的值 
* return url 参数替换后的url 
*/ 
function changeURLArg(url,arg,arg_val){ 
	if(url.endWith("#")){
		url = url.replace("#","");
	}
    var pattern=arg+'=([^&]*)'; 
    var replaceText=arg+'='+arg_val; 
    if(url.match(pattern)){ 
        var tmp='/('+ arg+'=)([^&]*)/gi'; 
        tmp=url.replace(eval(tmp),replaceText); 
        return tmp; 
    }else{ 
        if(url.match('[\?]')){ 
            return url+'&'+replaceText; 
        }else{ 
            return url+'?'+replaceText; 
        } 
    } 
    return url+'\n'+arg+'\n'+arg_val; 
};

String.prototype.endWith=function(s){
	  if(s==null||s==""||this.length==0||s.length>this.length)
	     return false;
	  if(this.substring(this.length-s.length)==s)
	     return true;
	  else
	     return false;
	  return true;
};

String.prototype.startWith=function(s){
	  if(s==null||s==""||this.length==0||s.length>this.length)
	   return false;
	  if(this.substr(0,s.length)==s)
	     return true;
	  else
	     return false;
	  return true;
};

//为jquery扩展一个能取得url中某个参数的方法
(function ($) {
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]); return null;
    }
})(jQuery);