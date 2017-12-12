jQuery(document).ready(function() {
    "use strict";
	// Django��Ҫ��֤csrf��Ϣ��֤�ύ�����ݣ���δ�����룬��Ҫ���빫��JS
	// csrf��Ϣ��ʼ
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
		// csrf��Ϣ����
});


/***
	Common functions
***/
$(function(){
    $.ajaxSetup ({
        cache: false //�ر�AJAX����
    });
});

//�����ĵ���ajax����
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
				alert('Sorry.An error occured.Please try again.');
			}
	});
};
//���ص�������ajax����ͨ�÷���
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
				alert('Sorry.An error occured.Please try again.');
			}
	});
};

jQuery(document).ready(function(e){
	item_count = $.cookie('cart_item_type_count')==null ? 0:$.cookie('cart_item_type_count');
	$(".top-cart-num-link").text(item_count);
});

//��껬�������Ĺ��ﳵ����ʱ���¼�
jQuery(".top-cart-num-link").hover(function(e){
	var url = '/cart/show/';
	var triggerControl = $(this);
	imycartAjaxCallWithCallback(url,null,imycartAjaxGetCartInfoCallback,triggerControl,null);
});

function imycartAjaxGetCartInfoCallback(result,triggerControl,extraInfo){
	if(result.success==true){
		triggerControl.text(result.item_type_count);
		$.cookie('cart_item_type_count',result.item_type_count,{expires: 365,path:'/'});
	}
};


//�ύѯ������
jQuery("#inquiry-submit").click(function(event){
	event.preventDefault();
	url = '/inquiry/add/'
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$('#inquiryForm').serialize(),
		async: false,
		error: function(request) {
			alert('Sorry.An error occured.Please try again.');
		},
		success: function(result){
			$("#infoMessage").html(result.message);
			$("#myModal").modal('toggle');
		}
	});
});




//�л�����
jQuery(".change_locale_btn").click(function(event){
	event.preventDefault();
	$("#changeLocaleForm").submit();
});


//�����ʼ��б�
jQuery(".add-to-emaillist").click(function(event){
	event.preventDefault();
	var email = new Object();
	email.email = $("#newsletter-email").val();
	var url = "/email-list/add/"
	imycartAjaxCall(url,email,true,null);
});

//��ݹ�˾ѡ��
jQuery(":radio[name='express']").click(function(){
	//alert("express changed")
	var url = '/cart/re-calculate-price/';
	$.ajax({
		cache: false,
		type: "GET",
		url:url,
		data:$("#place_order_form").serialize(),
		async: false,
		error: function(request) {
			alert('Sorry.An error occured.Please try again.');
		},
		success: function(data) {
			if(data.success==true){
				//alert(data.message.total);
				//alert("data.message.total:" + data.message.total);
				$("#sub_total_amount").text(data.message.sub_total.toFixed(2));
				$("#total_amount").text(data.message.total.toFixed(2));
				$("#discount_amount").text(data.message.discount.toFixed(2));
				$("#shipping_amount").text(data.message.shipping.toFixed(2));
			}
		}
	});
});

//�����Ż���
jQuery(".try-promotion-code").click(function(e){
	var url = "/promotion/?code="+$("#promotion_code").val();
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$("#place_order_form").serialize(),
		async: false,
		error: function(request) {
			alert('Sorry.An error occured.Please try again.');
		},
		success: function(data) {
			if(data.success==true){
				$("#total_amount").text(data.total.toFixed(2));
				$("#discount_amount").text(data.discount_amount.toFixed(2));
			}
		}
	});
});

//ÿҳ��ʾ��������
jQuery(".pageSize").click(function(event){
	event.preventDefault();
	var url = location.href;
	var newurl = changeURLArg(url,"pageSize",$(this).data("page-size"));
	location.href = newurl;//��ת����Ӧ��ҳ��
});


//ҳ������л�
jQuery(".pageChage").click(function(event){
	event.preventDefault();//��ֹA��ǩ��ת
	var url = location.href;
	var pageNo = $.getUrlParam("page");
	var tag = $(this).attr("data-tag");
	if(tag=="Previous"){
		//��ǰ�������ǰ���ǵ�һҳ������ǰ��ҳ
		if(pageNo>1){
			pageNo--;
			var newurl = changeURLArg(url,"page",pageNo);
			location.href = newurl;//��ת����Ӧ��ҳ��
		}
	}else if(tag=="Next"){
		//��������ǰ�������һҳ����ҳ
		var pages = $(this).data("page-range");
		if(pageNo<pages){
			pageNo++;
			var newurl = changeURLArg(url,"page",pageNo);
			location.href = newurl;//��ת����Ӧ��ҳ��
		}
	}else{
			var page = $(this).data("page");
			var newurl = changeURLArg(url,"page",page);
			location.href = newurl;//��ת����Ӧ��ҳ��
	}
});

//��ĳ������
jQuery(".orderBy").click(function(){
	event.preventDefault();//��ֹA��ǩ��ת
	var url = location.href;
	var newurl = changeURLArg(url,"sort_by",$(this).data("column"));
	location.href = newurl;//��ת����Ӧ��ҳ��
});

//������
jQuery(".sortDirection").click(function(event) {
	event.preventDefault();//��ֹA��ǩ��ת
	var url = location.href;
	var sp = $(this).find("span");
 	//var csss = sp.attr("class");
	if(sp.hasClass("glyphicon-arrow-up")){
		var newurl = changeURLArg(url,"direction","desc");
		sp.removeClass("glyphicon-arrow-up");
		sp.addClass("glyphicon-arrow-down");
		location.href = newurl;//��ת����Ӧ��ҳ��
	}else{
		var newurl = changeURLArg(url,"direction","asc");
		sp.removeClass("glyphicon-arrow-down");
		sp.addClass("glyphicon-arrow-up");
		location.href = newurl;//��ת����Ӧ��ҳ��
	}
});

//ˢ����֤��
jQuery(".next-captcha").click(function(event){
	event.preventDefault();
	$.getJSON('/refresh-captcha', function(json) {  
		// This should update your captcha image src and captcha hidden input  
		// debugger; 
		var status = json['status'];  
		var new_cptch_key = json['new_cptch_key'];  
		var new_cptch_image = json['new_cptch_image'];  
		id_captcha_0 = $("#id_reg_captcha_0");  
		img = $(".captcha");  
		id_captcha_0.attr("value", new_cptch_key);  
		img.attr("src", new_cptch_image);  
	});   
});

//ajax��֤��֤��
jQuery('.form-control-captcha').blur(function(){
	key_id = $(this).data('captcha-key')
	json_data={'response':$(this).val(),  
		// ��ȡ�����������ֶ�id_captcha_0����ֵ            
			'hashkey':$('#' + key_id).val()        
	};
	
	$.getJSON('/ajax_val_captcha', json_data, function(data){ //ajax����            
		$('#captcha_status').remove();            
		if(data['success'] == true){ //status����1Ϊ��֤����ȷ�� status����0Ϊ��֤����� �������ĺ���д����ʾ��Ϣ               
			//alert(data['message']);        
		}else{
			//alert(data['message']);
			//$(this).after('<span id="captcha_status" >*' + data['message'] + '</span>')     
		}        
	});     
});

/***
 ***   ҳ����ת�࿪ʼ
 ***/
jQuery("#CreateAccount").click(function(event) {
		location.href = "/user/register";
}); 

jQuery(".return-to-cart").click(function() {
	var url = "/cart/show";
	location.href = url;
});
/***
 ***   ҳ����ת�����
 ***/
 
//���ﳵ����
jQuery(".cart-qty").blur(function(e){
	var cp_id = $(this).data('cartid');
	var qty = $(this).val();
	imycartModifyCart('set',cp_id,qty,$(this));
});

jQuery(".qty-decrease").click(function(e){
	var cp_id = $(this).data('cartid');
	var current_qty = $("#cartqty-" + cp_id).val();
	if(current_qty<=1){
		return;
	}else{
		var qty = current_qty-1;
		imycartModifyCart('set',cp_id,qty,$(this));
		//$("#cartqty-" + cp_id).val(qty);
	}
});

jQuery(".qty-increase").click(function(e){
	var cp_id = $(this).data('cartid');
	var current_qty = $("#cartqty-" + cp_id).val();
	var qty = parseInt(current_qty)+1;
	imycartModifyCart('set',cp_id,qty,$(this));
	//$("#cartqty-" + cp_id).val(qty);
});

jQuery("[title^=Qty]").blur(function(event) {
	var cartid = $(this).attr("data-cartid");
	var quantity = $(this).val();
	if( quantity == 0){
		quantity = 1;
		$(this).val(1);
	}
	imycartModifyCart('set',cartid,quantity,$(this));
});

jQuery("[title^=Delete]").click(function(event) {
	event.preventDefault();
	var cartid = $(this).attr("data-cartid");
	imycartModifyCart('del',cartid,0,$(this));
});

jQuery("#empty_cart_button").click(function(event) {
	var cartid = $(this).attr("data-cartid");
	imycartModifyCart('clear',cartid,0,$(this));
}); 
 
 


/***
 ***  �鿴���ﳵ��ϸҳ��ʹ�õķ�����ʼ ***
 ***/
function imycartModifyCart(method,cart_id,quantity,triggerControl){
	url = '/cart/modify';
	var cart = new Object();
	cart.method = method;
	cart.cart_id = cart_id;
	cart.quantity = quantity;
	
	extraInfo = new Object();
	extraInfo.method = method;
	extraInfo.quantity_origin = quantity;
	extraInfo.cart_id = cart_id;
	imycartAjaxCallWithCallback(url,cart,imycartModifyCartCallback,triggerControl,extraInfo);
};

function imycartModifyCartCallback(result,triggerControl,extraInfo){
	flag = false;
	if(extraInfo.method=="set"){
		if(result.success==true){
			$("#price-" + extraInfo.cart_id).text("$" + result.cart_product_total.toFixed(2));
			$("#cartqty-" + extraInfo.cart_id).val(extraInfo.quantity_origin);
			flag = true;
		}else{
			triggerControl.val(result.origin);
			$("#infoMessage").html(result.message);
			$("#myModal").modal('toggle');
		}
		
	}else if(extraInfo.method == "del"){
		var tr = triggerControl.parent().parent();	
		tr.remove();
		flag = true;
		$(".top-cart-num-link").text(result.cart_item_type_count);
	}else if(extraInfo.method == "clear"){
		//�����
		flag = true;
		$(".carts-item").remove();
		$(".top-cart-num-link").text(result.cart_item_type_count);
	}

	//�����ܽ��
	if(flag){
		imycartUpdateTotalAmount(result.sub_total,result.sub_total);
	}
};

function imycartUpdateTotalAmount(totalAmount,totalPrice){
	//������Ʒ�ܼۡ����˷ѡ��ܽ��
	$("#totalPrice").html("$ " + totalPrice.toFixed(2));
	$("#totalAmount").html("$ " + totalAmount.toFixed(2));
};
/***
 ***  �鿴���ﳵ��ϸҳ��ʹ�õķ������� ***
 ***/
//���ť
jQuery(".order-pay-button").click(function(event) {
	var url = '/cart/payment/' + $(this).data("id");
	location.href = url;
}); 


//��ַѡ��
jQuery(".check-choice-address").click(function () {
	$(".check-address-list").show();
});


//���ĳ����ַ�����������˵��������������������
//���ڶ�̬���ӵ�li���󶨵�click�¼���ʧЧ��������������on('click','li>a',function(e))��д��
jQuery(".check-address-list").on('click','li>a',function(e){
	var str = new String($(this).text());
	$(".check-address-list").hide();
	$("#span_address_selected").text(str);
	var address_id = $(this).data("address-id");
	
	$(".input-address-id").val(address_id);
	$.updateAddressForm(address_id);
});

//jQuery(".check-address-list a").click(function (e) {
	//var str = new String($(this).text());
	//$(".check-address-list").hide();
	//$("#span_address_selected").text(str);
	//var address_id = $(this).data("address-id");
	
	//$(".input-address-id").val(address_id);
	//$.updateAddressForm(address_id);
//});



//��ַ�������޸�
jQuery(".btn-address-submit").click(function(){
	//����ť����Ϊ������
	$(this).attr('disabled',true);
	
	//var address_id = $("#select_address_id").val();
	var $form = $("#address-form").data('bootstrapValidator'); 
	$form.validate();
	var flag = $form.isValid();
	if(!flag){
		return;
	}
	//alert(flag);
	
	
	var submit_method = "dropdown_list";
	if (!($(this).data("submit-method") == "" || $(this).data("submit-method") == null)){
		submit_method = $(this).data("submit-method");
	}
	
	var address_id = $("#input_address_id").val();
	var url = "/user/address/opration/";
	if (address_id == ""){
		//˵��������
		url = url + "add/";
	}else{
		url = url + "modify/";
	}
	
	$.ajax({
		cache: false,
		type: "POST",
		url:url,
		data:$('#address-form').serialize(),
		async: false,
		error: function(request) {
			alert('Sorry.An error occured.Please try again.');
		},
		success: function(data) {
			if(data.success==true){
				if (submit_method == "dropdown_list"){
					var address_id = data.address.id;
					var useage = data.address.useage;
					var changeFlag = false;
					$("#ul_address_list li").each(function(){
						if($(this).find("a").data("address-id")==address_id){
							changeFlag = true;
							var html = "<a class='address-option' data-address-id='" + address_id + "'>" + useage + "</a>"
							$(this).html(html);
							//alert("TODO:Opration success:" + html);
						}
					});
					$("#span_address_selected").text(useage);
					
					if (!changeFlag){
						//������

						$("#ul_address_list").append("<li><a class='address-option' data-address-id='" + address_id + "'>" + useage + "</a></li>");
						$("#span_address_selected").text(useage);
						$(".input-address-id").val(address_id);


					}
				}else if(submit_method=="close_self"){
					//��ʱɶ������
					location.href = "/user/address/show/"
				}
			
			$(this).attr('disabled',false);
			}else{
				$(this).attr('disabled',false);
				if (submit_method == "dropdown_list" || submit_method == "close_self" ){
					$("#infoMessage").html(data.message);
					$("#myModal").modal('toggle');
				}
			}
			
		}
	});
});

//��ַѡ����޸�
$("#select_address_id").change(function(e){
	var address_id = $("#select_address_id").val();
	$.updateAddressForm(address_id);
});

$.updateAddressForm = function(address_id){
	//��ȡ��ַ����ϸ��Ϣ
	var url = "/user/address/detail/";
	
	if (address_id == ""){
		//���������б�
		//$("#address-form")[0].reset(); 
		//���ñ���Ҫ�Ӹ�[0],����Ķ�����������
		//����reset�����и����⣬���input����value="xx",��ôֻ�ܻ�ԭ��xx
		$(':input','#address-form')  
			.not(':button, :submit, :reset, :hidden')  
			.val('')  
			.removeAttr('checked')  
			.removeAttr('selected'); 
	}else{
		url = url + address_id;
		$.ajax({
			cache: false,
			type: "GET",
			url:url,
			data:null,
			async: false,
			error: function(request) {
				alert('Sorry.An error occured.Please try again.');
			},
			success: function(data) {
				if(data.success==true){
					for (key in data.address){
						$("#id_" + key).val(data.address[key]); //ҳ����input���������� "id_�ֶ�"����ʽ
					}
				}

			}
		});
	}
	
	//����������֤״̬
	$("#address-form").data('bootstrapValidator').resetForm();
};

//�µ�
jQuery(".btn-place-order").click(function(e){
	//����ַ��û��ѡ��
	var address_id = $("#input_address_id").val();
	if (address_id>0){
		$("#place_order_form").submit();
	}else{
		$("#infoMessage").html("Please choose a shipping address.");
		$("#myModal").modal('toggle');
	}
	
	
});

 
//ȡ������
jQuery(".order-cancel-button").click(function(event) {
	var url = '/order/cancel';
	var object = new Object();
	object.order_id = $(this).data("id");
	
	var extraInfo = new Object();
	extraInfo.method = 'cancel';
	extraInfo.order_id = object.order_id;
	imycartAjaxCallWithCallback(url,object,imycartChangeOrderCallBack,$(this),extraInfo)	
}); 


//�û���Ϣ
jQuery("#changePassword").click(function(){
    if ($("#changePassword").attr('checked')){
        $(".change-password").hide();
        $("#changePassword").removeAttr('checked');
    }
    else{
        $("#changePassword").attr('checked','true');
        $(".change-password").show();
    }
});


jQuery(".btn-userinfo-submit").click(function(e){
	var $form = $("#userInfoForm").data("bootstrapValidator");
	$form.validate();
	if ($form.isValid()){
		$("#userInfoForm").data("bootstrapValidator").defaultSubmit();
	}
	
});

function imycartChangeOrderCallBack(result,triggerControl,extraInfo){
	if(extraInfo.method=='cancel'){
		//ɾ���Լ���һ��
		condition = "[title=" + "container_order_" + extraInfo.order_id + "]";
		$(condition).remove();
	}
};


//����Ʒ���ӵ����ﳵ	
jQuery("#addToCartBtn").click(
	function() {
		var productId = $(this).data("product-id");
		
		var product_attribute_id = $("#product-attribute-id").val();
		//���û�н���Ʒ����ѡ��ȫ�棬�������ύ
		
		if($(".product-attribute-group-div").length > 0){
			if (product_attribute_id){
				imycartAddProductToCart(productId,product_attribute_id,$("#qty").val(),imycartAddProductToCartCallBack,this,null);
			}else{
				//��һ��������ͻ�Ҳѡ�˵��Ǻ�̨����SKUû�У�������������ڱ���2����ɫ��2�в�����ϣ�����Ӧ����4����ϣ����Ǻ�̨ɾ����һ�֣�
				var select_all_group = true;
				$(".product-attribute-group-div").each(function(index,div){
					if (!($(div).find(".product-attribute-group-selected").val())){
						$("#infoMessage").html("Please select " + $(div).data("attribute-group-name") + ".");
						select_all_group = false;
						//break;
						return false;
					}		
				});
				if (select_all_group){
					$("#infoMessage").html("This sku is nolonger on sale.");
				}
				$("#myModal").modal('toggle');
			}
		}else{
			imycartAddProductToCart(productId,product_attribute_id,$("#qty").val(),imycartAddProductToCartCallBack,this,null);
		}
	}
);

function imycartAddProductToCart(product_id,product_attribute_id,quantity,callback,triggerControl,extraInfo){
		var url = "/cart/add";
		var cart = new Object();
		cart.product_id = product_id;
		cart.product_attribute_id = product_attribute_id;
		cart.quantity = quantity;
		
		imycartAjaxCallWithCallback(url,cart,callback,triggerControl,extraInfo)
		//imycartAjaxCall(url,cart,true,'showservermessage');
};

function imycartAddProductToCartCallBack(result,triggerControl,extraInfo){
	if (result.success == true){
		location.href = "/cart/show/";
		//$.addcartFlyEfect(triggerControl);
	}else{
		$("#infoMessage").html(result.message);
		$("#myModal").modal('toggle');
	}
};

//����Ʒ���ӵ�Ը���嵥
jQuery("#addToWishList").click(
	function(event) {
		event.preventDefault();
		imycartAddProductToWishlist($(this).data("product-id"),$(this),null);
	}
);
function imycartAddProductToWishlist(product_id,triggerControl,extraInfo) {
	var url = "/wishlist/add";
	var wish = new Object();
	wish.product_id = product_id;
	imycartAjaxCallWithCallback(url,wish,imycartAddProductToWishlistCallBack,triggerControl,extraInfo);
};

function imycartAddProductToWishlistCallBack(result,triggerControl,extraInfo){
	if(result.success==true){
		$(".detail-heart").addClass("detail-heart-click");
		$("#infoMessage").html(result.message);
		$("#myModal").modal('toggle');
	}else{
		if(result.message=="needLogin"){
			location.href = "/user/login/?next=" + result.next;
		}
	}
};

//����Ʒ��Ը���嵥ɾ��
jQuery(".remove-from-wishlist").click(
	function(event) {
		event.preventDefault();
		var extraInfo = new Object();
		extraInfo.topDivId = $(this).data("top-div-id");
		imycartRemoveProductFromWishlist($(this).data("wishlistid"),$(this),extraInfo);
	}
);

function imycartRemoveProductFromWishlist(wish_id,triggerControl,extraInfo){
			var url = "/wishlist/remove";
			var wish = new Object();
			wish.id = wish_id;
			var encodedata = $.toJSON(wish);
			imycartAjaxCallWithCallback(url,wish,imycartRemoveProductFromWishlistCallBack,triggerControl,extraInfo);
};

function imycartRemoveProductFromWishlistCallBack(result,triggerControl,extraInfo){
	if(result.success==true){
		$("#" + extraInfo.topDivId ).remove();
	}else{
		$("#infoMessage").html(result.message);
		$("#myModal").modal('toggle');
	}
};	


//ѡ������Ʒĳ����������
jQuery(".product-attribute-item").click(function(){
		//�жϵ�ǰ������Ƿ�����Чѡ��
		if ($(this).parent().hasClass("sku-inavailable")||$(this).parent().hasClass("sku-text-inavailable")){
			return;
		}
	
		//�жϵ�������Ѿ�ѡ�еĻ���ûѡ�е�
		condition = ".product-attribute-group-selected[title=" + $(this).data("group-code") + "]";
		
		if ($(this).parent().hasClass("redborder")){
			/*  ����Ʒȥ����ʾѡ�к����߼� */
			$(this).parent().prevAll().removeClass('redborder');
			$(this).parent().nextAll().removeClass('redborder');
			$(this).parent().removeClass('redborder');
			$(condition).val("");
		}else{
			/*  ����Ʒ���ϱ�ʾѡ�к����߼� */
			$(this).parent().prevAll().removeClass('redborder');
			$(this).parent().nextAll().removeClass('redborder');
			$(this).parent().addClass('redborder');
			$(condition).val($(this).data("attribute-id"));
		}
			
	
		var product_to_get = new Object();
		product_to_get.product_id = $(this).data("product-id");

		var attr_list = new Array();
		$(".product-attribute-group-selected").each(function(){
			if($(this).val() != ""){
				attr_list.push($(this).val());
			}
			
		});
		product_to_get.attr_list = attr_list;
		var url = '/product/get-product-extra/'
		var encodedata = $.toJSON(product_to_get);
		$.ajax({
				type : 'POST',
				contentType : 'application/json',
				dataType : 'json',
				url : url,
				data : encodedata,
				success : function(result) {
						if(result.success==true){
							$("#product-attribute-id").val(result.message.pa_id);
							$("#min_order_quantity").text(result.message.min_order_quantity);
							//ȷ���۸�
							$("#product-price-main").text("$" + result.message.price.toFixed(2));
							
							//������ʾ�Ĵ�ͼ
							if (result.message.show_image==true){
								$("#product-big-image").attr("jqimg",result.message.image_url);
								$("#product-big-image").attr("src",result.message.image_url);
							}
						}else{
							//�趨����ѡ��������б�
							//alert('Attributs avaliable to select are:' + result.message)
							//$(".product-attribute-item").attr("disabled",true);
							//$(".product-attribute-item").addClass("disabled");
							
							$(".attr-text").removeClass("sku-text-available");
							$(".attr-text").addClass("sku-text-inavailable");

							$(".attr-img").removeClass("sku-available");
							$(".attr-img").addClass("sku-inavailable");
							
							
							var id_and_type = result.not_selected;
							
							if($.trim(id_and_type)!=""){
								id_list = String(id_and_type).split(",");
								$.each(id_list,function(index,id){
									tmp = id.split("|")
									var available_class_name = 'sku-available';
									var inavailable_class_name = 'sku-inavailable';
									if (tmp[1]=='text'){
										available_class_name = 'sku-text-available';
										inavailable_class_name = 'sku-text-inavailable';
									}
									$("[data-attribute-id=" + tmp[0] + "]").parent().removeClass(inavailable_class_name);
									$("[data-attribute-id=" + tmp[0] + "]").parent().addClass(available_class_name);
								});
							}
							
							
							id_and_type = result.selected;
							if ($.trim(id_and_type)!=""){
								id_list = String(id_and_type).split(",");
								$.each(id_list,function(index,id){
									tmp = id.split("|")
									var available_class_name = 'sku-available';
									var inavailable_class_name = 'sku-inavailable';
									if (tmp[1]=='text'){
										available_class_name = 'sku-text-available';
										inavailable_class_name = 'sku-text-inavailable';
									}
									$("[data-attribute-id=" + tmp[0] + "]").parent().removeClass(inavailable_class_name);
									$("[data-attribute-id=" + tmp[0] + "]").parent().addClass(available_class_name);
								});
							}						
						}
						//alert('pa_id:' + $("input[name=product-attribute-id]").val());
				},
				error : function(result) {
					alert('Sorry.An error occured.Please try again.');
				}
		}); 
});


/* 
* url Ŀ��url 
* arg ��Ҫ�滻�Ĳ������� 
* arg_val �滻��Ĳ�����ֵ 
* return url �����滻���url 
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

//Ϊjquery��չһ����ȡ��url��ĳ�������ķ���
(function ($) {
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]); return null;
    }
})(jQuery);