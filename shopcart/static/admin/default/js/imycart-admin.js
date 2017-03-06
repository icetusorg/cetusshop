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

//通用弹出窗口

jQuery(".common-popup-trigger").click(function () {
    $("#common-pop-frame").attr("src", $(this).attr("data-target-url"));    // 设定当前框架iframe 的地址为 该链接地址
	$('.cd-popup.common-pop-win').addClass('is-visible');
});

//close popup
jQuery('.cd-popup').on('click', function(event){
	if( $(event.target).is('.cd-popup-close') || $(event.target).is('.cd-popup') || $(event.target).is('.cd-popup-close-btn') ) {
		event.preventDefault();
		$(this).removeClass('is-visible');
	}
});



//下拉菜单选项切换
jQuery(".dropdown-item").click(function(){
	var select_text = $(this).text();	
	var value = $(this).data("value");
	//可以接收一个后续的函数，做出额外的处理
	var extra_func = $(this).data("func");
		
	$(this).parent().parent().find(".inputBtn").find(".selected-text").text(select_text);
	$(this).parent().parent().find(".dropdown-item-input").val(value); // 将选中的值放入隐藏的input
	
	
	if (extra_func != '' && extra_func != null && extra_func != undefined){
		//alert(extra_func);
		fn = eval(extra_func);
	    fn.call(this,value);
	}
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

jQuery("#main-content-btn-all").click(function(event){
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
jQuery(".pageChage").click(function(event){
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

//页码跳转
jQuery(".page-jump").click(function(event){
	event.preventDefault();//阻止A标签跳转
	var url = location.href;
	var pageNo = $.getUrlParam("page");
	var tag = $(this).attr("data-tag");
	try{
		pageNo = "1";
		$(this).parent().find("input[name=page_number_to_jump]").each(function(){
			pageNo = ($(this).val());
		});
	}catch(err){
		pageNo = "1";
	}
	
	var newurl = changeURLArg(url,"page",pageNo);
	location.href = newurl;//跳转到对应的页面

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

//订单动作类
jQuery("#admin_pay_order").click(function(event){
	event.preventDefault();//阻止A标签跳转
	$("#infoMessage").html("本功能正在开发中，敬请期待。");
	$("#myModal").modal('toggle');
});

jQuery("#collect_order_products").click(function(event){
	event.preventDefault();//阻止A标签跳转
	o_status = "collected";
	order_id = $(this).data("order-id");
	modify_order_status(o_status,order_id);
});

jQuery("#ship_order_products").click(function(event){
	event.preventDefault();//阻止A标签跳转
	//$("#infoMessage").html("本功能正在开发中，敬请期待。");
	//$("#myModal").modal('toggle');
	$(".tag li,.add-content").removeClass("active");
	$(".tag_shippment").addClass("active");
	$("#tag_shippment").addClass("active");
	
});

jQuery("#return_money").click(function(event){
	event.preventDefault();//阻止A标签跳转
	$("#infoMessage").html("本功能正在开发中，敬请期待。");
	$("#myModal").modal('toggle');
});

jQuery("#return_order_products").click(function(event){
	event.preventDefault();//阻止A标签跳转
	$("#infoMessage").html("本功能正在开发中，敬请期待。");
	$("#myModal").modal('toggle');
});

jQuery("#close_order").click(function(event){
	event.preventDefault();//阻止A标签跳转
	o_status = "closed";
	order_id = $(this).data("order-id");
	modify_order_status(o_status,order_id);
});

jQuery("#finish_order").click(function(event){
	event.preventDefault();//阻止A标签跳转
	o_status = "finished";
	order_id = $(this).data("order-id");
	modify_order_status(o_status,order_id);
});

jQuery("#edit_order").click(function(event){
	event.preventDefault();//阻止A标签跳转
	$("#infoMessage").html("本功能正在开发中，敬请期待。");
	$("#myModal").modal('toggle');
});

function modify_order_status(order_status,order_id){
	var url = "/admin/order-status/{status}/{order_id}/";
	url = url.replace("{status}",order_status);
	url = url.replace("{order_id}",order_id);
	
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
			$("#infoMessage").html(data.message);
			$('#myModal').on('hidden.bs.modal', function (e) {
				var url = location.href;
				//var newurl = changeURLArg(url,"tab_name","tag_remark");
				location.href = url;//跳转到对应的页面
			});
			
			$("#myModal").modal('toggle');
		}
	});
	
};


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
				var newurl = changeURLArg(url,"tab_name","tag_remark");
				location.href = newurl;//跳转到对应的页面
			});
			
			$("#myModal").modal('toggle');
			
		}
	});
});

//订单详情tab页切换
jQuery(".tag li").on("click", function () {
    var contentId = $(this).attr("data");
    $(".tag li,.add-content").removeClass("active");
    $(this).addClass("active");
    $("#" + contentId).addClass("active");
});


//发货记录删除
jQuery(".delete-ship-record").click(function(){
	var url = "/admin/order-shippment-manage/delete/";
	var id = $(this).data("id");
	url = url + id + "/";

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
			$("#infoMessage").html(data.message);
			$('#myModal').on('hidden.bs.modal', function (e) {
				var url = location.href;
				var newurl = changeURLArg(url,"tab_name","tag_shippment");
				location.href = newurl;//跳转到对应的页面
			});
			
			$("#myModal").modal('toggle');
			
		}
	});	
});


//文章管理界面
//文章管理批量操作
jQuery(".article-batch-oper").click(function(e){
	var url = "/admin/article-";
	method = $(this).data("method");
	url = url + method + "/";

	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#article_batch_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					var newurl = location.href;
					location.href = newurl;
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});


//文章基本信息提交
jQuery("#article-basic-info-submit-btn").click(function(event){
	event.preventDefault();
	var url = "/admin/article-edit/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#article-basic-info-form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.href = url + "?id=" + data.data.article_id;
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});


//文章详细信息提交
jQuery("#article-detail-info-submit-btn").click(function(event){
	event.preventDefault();
	var url = "/admin/article-detail-manage/";
	//由于使用了ckeditor，直接获取文本域的值，会丢失修改部分的信息，因此要先用api获取修改以后的值填到文本域中
	
	var data = CKEDITOR.instances.article_content_editor.getData();
	$("#article_content_editor").val(data);
	//alert($("#editor").val())
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#article-detail-info-form").serialize(),
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

//文章图片
jQuery("#article-picture-manage-submit-btn").click(function(event){
	event.preventDefault();
	var url = "/admin/article-picture-manage/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#article_picture_manage_form").serialize(),
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

//文章分类管理
//分类详情提交
jQuery("#article_busi_catigory_detail_submit_btn").click(function(event){
	event.preventDefault();
	var url = "/admin/article-busi-category-edit/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#article_busi_catigory_detail_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.href = url + "?id=" + data.category_id;
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});

//文章分类批量操作
jQuery(".article-category-batch-oper").click(function(e){
	//自动选中选择的那行
	id = $(this).data("id");
	if(id != undefined){
		$("#checkbox_"+id).prop("checked", true);
	}
	
	var url = "/admin/article-busi-category-";
	method = $(this).data("method");
	url = url + method + "/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#article_category_batch_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.reload(true); 
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});




//用户管理
//管理员详情
jQuery("#user_admin_detail_submit_btn").click(function(event){
	event.preventDefault();
	var url = "/admin/user-admin-edit/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#user_admin_detail_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				
			}
			$("#myModal").modal('toggle');
		}
	});
});

//用户管理批量操作
jQuery(".user-batch-oper").click(function(e){
	//自动选中选择的那行
	user_id = $(this).data("user-id");
	if(user_id != undefined){
		$("#checkbox_"+user_id).prop("checked", true);
	}
	
	var url = "/admin/user-";
	method = $(this).data("method");
	url = url + method + "/";

	if (method=='active'){
		url = url + $(this).data("status") + "/";
	}
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#user_batch_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.reload(true); 
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});




//商品管理界面
//Tab页切换方法
//添加商品，页签（基本信息-属性-相册）点击事件
jQuery(".product-info-tag li .article-info-tag li").on("click",function(){
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


//生成商品参数按钮
jQuery("#make_product_para").click(function(){
	var url = "/admin/product-para-detail-create/";

	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#product_para_detail_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			$('#myModal').on('hidden.bs.modal', function (e) {
				var url = location.href;
				var newurl = changeURLArg(url,"tab_name","tag_product_para");
				location.href = newurl;//跳转到对应的页面
			});
			
			$("#myModal").modal('toggle');
			
		}
	});
});

jQuery("#product_para_value_submit").click(function(){
	var url = "/admin/product-para-detail-edit/";

	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#product_para_detail_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			$('#myModal').on('hidden.bs.modal', function (e) {
				var url = location.href;
				var newurl = changeURLArg(url,"tab_name","tag_product_para");
				location.href = newurl;//跳转到对应的页面
			});
			
			$("#myModal").modal('toggle');
			
		}
	});
});




//商品分类选择
//修改了提交方式，这个方法没用了
//jQuery(".category-selection-checkbox").click(function(){
//	var category_id_list = new Array();
//	$("#product_category_selection").find("input[type='checkbox']").each(function(){
//		if ($(this).prop("checked")){
//			category_id_list.push($(this).data("cat-id"));
//		}
//	});
//	$("input[name='product_category_list']").val(category_id_list.join(","));
//});

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
				//itemArray.sort();
				
				var sortedArray = itemArray.sort(function(a,b){
					return a.name.localeCompare(b.name);
				});	
				
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
				var newurl = changeURLArg(url,"tab_name","tag_sku");
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
				var newurl = changeURLArg(url,"tab_name","tag_sku");
				location.href = newurl;//跳转到对应的页面
			});
			
			$("#myModal").modal('toggle');
			
		}
	});
	
});

//删除SKU
jQuery(".sku_delete_link").click(function(event){
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
				var newurl = changeURLArg(url,"tab_name","tag_sku");
				location.href = newurl;//跳转到对应的页面
			});
			
			$("#myModal").modal('toggle');
			
		}
	});
});


//商品参数组管理
jQuery(".product—para-group-batch-oper").click(function(e){
	var url = "/admin/product-para-group-";
	url =  url + $(this).data("method") + "/";
	
	id = $(this).data("id");
	if(id != undefined){
		$("#checkbox_"+id).prop("checked", true);
	}
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#product_para_group_batch_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					var newurl = location.href;
					location.href = newurl;
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});

//商品参数组保存
jQuery("#product_para_group_detail_submit").click(function(event){
	event.preventDefault();//阻止A标签跳转
	var url = "/admin/product-para-group-edit/"

	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#product_para_group_detail_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			$('#myModal').on('hidden.bs.modal', function (e) {
				var url = location.href;
				location.href = url;//跳转到对应的页面
			});
			
			$("#myModal").modal('toggle');
			
		}
	});
});

//商品SKU组保存
jQuery("#product_sku_group_detail_submit").click(function(event){
	event.preventDefault();//阻止A标签跳转
	var url = "/admin/product-sku-group-edit/"

	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#product_sku_group_detail_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			$('#myModal').on('hidden.bs.modal', function (e) {
				var url = location.href;
				location.href = url + "?id=" + data.sku_group_id;
			});
			
			$("#myModal").modal('toggle');
			
		}
	});
});



//商品图片管理

//文件上传与相册
//设为主图
jQuery("#product_main_picture_show").on('click',".set-picture-attr",function(event){
	event.preventDefault();
	var img_url = $(this).data("image-url");
	var type = $(this).data("image-type");
	var product_id = $(this).data("product-id");
	var picture_id = $(this).data("id");
	method = $(this).data("method");
	
	var url = "";
	if (type = "product"){
		url = "/admin/product-set-image/";
	}
	
	var postdata = {"product_id":product_id,"picture_id":picture_id,"method":method};
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:postdata,
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);			
			$("#myModal").modal('toggle');
			reload_picture_list();
		}
	});
});





//相册里删除图片
jQuery(".album-image-show").on('click',".set-picture-attr",function(event){
	event.preventDefault();
	var type = $(this).data("image-type");
	var product_id = $(this).data("product-id");
	var picture_id = $(this).data("id");
	method = $(this).data("method");
	
	var url = "";
	if (type = "product"){
		url = "/admin/product-set-image/";
	}
	
	var postdata = {"product_id":product_id,"picture_id":picture_id,"method":method};
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:postdata,
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					var newurl = location.href;
					location.href = newurl;
				})
			}			
			$("#myModal").modal('toggle');
			
		}
	});
	
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

//修改了顺序号，自动勾选



//产品管理批量操作
jQuery(".product-batch-oper").click(function(e){
	var url = "/admin/product-oper/";
	method = $(this).data("method");
	$("#product_batch_method").val(method);

	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#product_batch_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					var newurl = location.href;
					location.href = newurl;
				})
			}
			$("#myModal").modal('toggle');
		}
	});
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

//系统管理页面

//网站信息
jQuery("#site_config_submit_btn").click(function(e){
	var url = "/admin/site-config-manage/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#site_config_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.reload(true); 
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});

//显示设置
jQuery("#display_config_submit_btn").click(function(e){
	var url = "/admin/display-config-manage/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#display_config_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.reload(true); 
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});

//邮件设置
jQuery("#email_detail_config_submit_btn").click(function(e){
	var url = "/admin/email-config-manage/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#email_detail_config_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.reload(true); 
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});

//留言管理
//删除留言
jQuery(".inquiry-delete").click(function(e){
	var url = "/admin/inquiry-delete/";
	
	// 创建Form  
    //var myform = $('<form></form>'); 
	var $myform = $("<form>",{
					id:'inquiry_delete_form',
					});

	
	//判断来自单条删除的还是批量的删除 
	var inquiry_id = $(this).data("inquiry-id");
	if("batch"==inquiry_id){
		//批量的
		$("#main-content-table").find("input[type='checkbox']:checked").each(function(){
			var $input = $("<input>",{
							name:'inquiry_id',
							value:$(this).val(),
							}).appendTo($myform);
		});
		
	}else{
		var $input = $("<input>",{
					name:'inquiry_id',
					value:inquiry_id,
					}).appendTo($myform);
	}
    
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$myform.serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					var newurl = location.href;
					location.href = newurl;
				})
			}
			$("#myModal").modal('toggle');
		}
	});
	
});


//快递管理
//编辑快递方式
jQuery("#delivery_type_detail_submit_btn").click(function(e){
	var url = "/admin/delivery-type-edit/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#delivery_type_detail_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.href = url + "?id=" + data.express_type_id;
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});

//删除配送方式
jQuery(".delete-delivery-type").click(function(e){
	var url = "/admin/delivery-type-delete/";
	var type_id = $(this).data("id");
	url = url + type_id + "/";
	
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
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.reload(true); 
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});


//编辑快递公司
jQuery("#express_detail_submit_btn").click(function(e){
	var url = "/admin/express-edit/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#express_detail_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.href = url + "?id=" + data.express_id;
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});

//删除快递公司
jQuery(".detele-express").click(function(e){
	var url = "/admin/express-delete/";
	var express_id = $(this).data("id");
	url = url + express_id + "/";
	
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
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.reload(true); 
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});


//支付方式设置
//提交设置
jQuery(".pay-config-submit-btn").click(function(e){
	var url = "/admin/pay-config/";
	var pay_type = $("input[name=pay_type]").val();
	url = url + pay_type + "/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$(this).parent().parent().serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.reload(true); 
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});

//分类管理编辑

//提交
jQuery("#category_detail_submit_btn").click(function(e){
	var url = "/admin/category-edit/";
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#category_detail_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					location.reload(true); 
				})
			}
			$("#myModal").modal('toggle');
		}
	});
});

//自定义URL详情
//跳转方式切换的变化
function jump_type_extra(type){
	if (type=='MVC'){
		 $("#page_deitor_jump_div").css("display", "none");
	}else{
		$("#page_deitor_jump_div").css("display", "block");
	}
}


//提交设置
jQuery("#customize_url_detail_submit_btn").click(function(event){
	event.preventDefault();
	var url = "/admin/customize-url-detail/{id}/";
	
	id = $(this).data("id");
	
	url = url.replace("{id}",id)
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#customize_url_detail_form").serialize(),
		async: false,
		error: function(request) {
			alert("System error");
		},
		success: function(data) {
			$("#infoMessage").html(data.message);
			if(data.success==true){
				$('#myModal').on('hidden.bs.modal', function (e) {
					var newurl = location.href;
					location.href = newurl;
				})
			}
			$("#myModal").modal('toggle');
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