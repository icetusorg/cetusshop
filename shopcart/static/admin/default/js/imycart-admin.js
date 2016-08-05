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