$(document).ready(function () {
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
        console.log("cookieValue_csrftoken:" + cookieValue)
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        cache: false //关闭AJAX缓存
    });
    // csrf信息结束

    //公共的调用ajax方法

    function imycartAjaxCall(url, object, is_show_message_box, message) {
        var encodedata = $.toJSON(object);
        $.ajax({
            beforeSend: function (xhr, settings) {
                console.log("Start to set csrftoken.......");
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    console.log("Set the csrf token successful.");
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            url: url,
            data: encodedata,
            success: function (result) {
                if (result.success == true) {
                    if (is_show_message_box) {
                        if (message == null) {
                            message = "Your opration is success.";
                        } else if (message == 'showservermessage') {
                            message = result.message;
                        }
                        $("#infoMessage").html(message);
                    }
                } else {
                    if (message == null) {
                        message = "Your opration is failed.";
                    } else if (message == 'showservermessage') {
                        message = result.message;
                    }
                    $("#infoMessage").html(message);
                }
                $("#myModal").modal('toggle');
            },
            error: function (result) {
                alert('Sorry.An error occured.Please try again.');
            }
        });
    };

//带回调函数的ajax请求通用方法

    function imycartAjaxCallWithCallback(url, object, callback, triggerControl, extraInfo) {
        var encodedata = $.toJSON(object);
        $.ajax({
            beforeSend: function (xhr, settings) {
                console.log("Start to set csrftoken.......");
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    console.log("Set the csrf token successful.");
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            url: url,
            data: encodedata,
            success: function (result) {
                callback(result, triggerControl, extraInfo);
            },
            error: function (result) {
                alert('Sorry.An error occured.Please try again.');
            }
        });
    };


//把商品添加到购物车
    jQuery("#addToCartBtn").click(
        function () {
            var productId = $(this).data("product-id");

            var product_attribute_id = $("#product-attribute-id").val();
            //如果没有将商品属性选择全面，则不允许提交

            if ($(".product-attribute-group-div").length > 0) {
                if (product_attribute_id) {
                    imycartAddProductToCart(productId, product_attribute_id, $("#qty").val(), imycartAddProductToCartCallBack, this, null);
                } else {
                    //有一种情况，客户也选了但是后台这种SKU没有（这种情况出现在比如2种颜色、2中材质组合，本来应该有4种组合，但是后台删除了一种）
                    var select_all_group = true;
                    $(".product-attribute-group-div").each(function (index, div) {
                        if (!($(div).find(".product-attribute-group-selected").val())) {
                            $("#infoMessage").html("Please select " + $(div).data("attribute-group-name") + ".");
                            select_all_group = false;
                            //break;
                            return false;
                        }
                    });
                    if (select_all_group) {
                        $("#infoMessage").html("This sku is nolonger on sale.");
                    }
                    $("#myModal").modal('toggle');
                }
            } else {
                imycartAddProductToCart(productId, product_attribute_id, $("#qty").val(), imycartAddProductToCartCallBack, this, null);
            }
        }
    );


    function imycartAddProductToCart(product_id, product_attribute_id, quantity, callback, triggerControl, extraInfo) {
        var url = "/quote/add";
        var cart = new Object();
        cart.product_id = product_id;
        cart.product_attribute_id = product_attribute_id;
        cart.quantity = quantity;

        imycartAjaxCallWithCallback(url, cart, callback, triggerControl, extraInfo)
        //imycartAjaxCall(url,cart,true,'showservermessage');
    };

    function imycartAddProductToCartCallBack(result, triggerControl, extraInfo) {
        if (result.success == true) {
            location.href = "/quote/show/";
            //$.addcartFlyEfect(triggerControl);
        } else {
            $("#infoMessage").html(result.message);
            $("#myModal").modal('toggle');
        }
    };

//公共方法
//下拉菜单选项切换
    jQuery(".dropdown-item").click(function () {
        var select_text = $(this).text();
        var value = $(this).data("value");
        $(this).parent().parent().find(".inputBtn").find(".selected-text").text(select_text);
        $(this).parent().parent().find(".dropdown-item-input").val(value); // 将选中的值放入隐藏的input
    });

//鼠标滑过顶部的购物车数量时的事件
    jQuery(".top-cart-num-link").hover(function (e) {
        var url = '/quote/show/';
        var triggerControl = $(this);
        imycartAjaxCallWithCallback(url, null, imycartAjaxGetCartInfoCallback, triggerControl, null);
    });

    function imycartAjaxGetCartInfoCallback(result, triggerControl, extraInfo) {
        if (result.success == true) {
            triggerControl.text(result.item_type_count);
            $.cookie('cart_item_type_count', result.item_type_count, {expires: 365, path: '/'});
        }
    };


    //提交询盘问题
    jQuery("#inquiry-submit").click(function (event) {
        event.preventDefault();
        var url = '/inquiry/add/';

        $.ajax({
            beforeSend: function (xhr, settings) {
                console.log("Start to set csrftoken.......");
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    console.log("Set the csrf token successful.");
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            cache: false,
            type: "POST",
            url: url,
            data: $('#inquiryForm').serialize(),
            async: false,
            error: function (request) {
                alert('Sorry.An error occured.Please try again.');
            },
            success: function (result) {
                $("#infoMessage").html(result.message);
                $("#myModal").modal('toggle');
            }
        });
    });

    //提交邮件订阅
    jQuery("#email-inquiry-submit").click(function (event) {
        event.preventDefault();
        var url = '/inquiry/email-add/';
        console.log("进入邮件订阅");
        $.ajax({
            beforeSend: function (xhr, settings) {
                console.log("Start to set csrftoken.......");
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    console.log("Set the csrf token successful.");
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            cache: false,
            type: "POST",
            url: url,
            data: $('#email_inquiryForm').serialize(),
            async: false,
            error: function (request) {
                alert('Sorry.An error occured.Please try again.');
            },
            success: function (result) {
                $("#infoMessage").html(result.message);
                $("#myModal").modal('toggle');
            }
        });
    });


    // 提交购物车询盘
    jQuery("#quote-submit").click(function (event) {
        event.preventDefault();
        var url = '/quote/add/';
        $.ajax({
            beforeSend: function (xhr, settings) {
                console.log("Start to set csrftoken.......");
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    console.log("Set the csrf token successful.");
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            cache: false,
            type: "POST",
            url: url,
            data: $('#inquiryForm').serialize(),
            async: false,
            error: function (request) {
                alert('Sorry.An error occured.Please try again.');
            },
            success: function (result) {
                $("#infoMessage").html(result.message);
                $("#myModal").modal('toggle');
            }
        });
    });


//切换语言
    jQuery(".change_locale_btn").click(function (event) {
        event.preventDefault();
        $("#changeLocaleForm").submit();
    });


//加入邮件列表
    jQuery(".add-to-emaillist").click(function (event) {
        event.preventDefault();
        var email = new Object();
        email.email = $("#newsletter-email").val();
        var url = "/email-list/add/"
        imycartAjaxCall(url, email, true, null);
    });

//快递公司选择（重新计算价格）
    jQuery(":radio[name='express'],#promotion_code_apply").click(function () {
        //alert("express changed")
        var url = '/cart/re-calculate-price/';
        var code_try = $("#promotion_code_try").val();
        $.ajax({
            beforeSend: function (xhr, settings) {
                console.log("Start to set csrftoken.......");
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    console.log("Set the csrf token successful.");
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            cache: false,
            type: "GET",
            url: url,
            data: $("#place_order_form").serialize(),
            async: false,
            error: function (request) {
                alert('Sorry.An error occured.Please try again.');
            },
            success: function (data) {
                if (data.success == true) {
                    if (data.is_promotion_code_valid == true) {
                        //优惠码有效
                        $("#promotion_code").val(code_try);
                        console.log("promotion_code:" + $("#promotion_code").val());
                    } else {
                        $("#promotion_code").val('');
                        $("#infoMessage").html(data.message);
                        $("#myModal").modal('toggle');
                    }
                    $("#sub_total_amount").text(data.prices.sub_total.toFixed(2));
                    $("#total_amount").text(data.prices.total.toFixed(2));
                    $("input[name=total]").val(data.prices.total.toFixed(2));
                    $("#discount_amount").text(data.prices.discount.toFixed(2));
                    $("input[name=discount]").val(data.prices.discount.toFixed(2));
                    $("#shipping_amount").text(data.prices.shipping.toFixed(2));
                    $("input[name=shipping]").val(data.prices.shipping.toFixed(2))
                }
            }
        });
    });


//每页显示数量设置
    jQuery(".pageSize").click(function (event) {
        event.preventDefault();
        var url = location.href;
        var newurl = changeURLArg(url, "pageSize", $(this).data("page-size"));
        location.href = newurl;//跳转到对应的页面
    });


//页数点击切换
    jQuery(".pageChage").click(function (event) {
        event.preventDefault();//阻止A标签跳转
        var url = location.href;
        var pageNo = $.getUrlParam("page");

        if (pageNo==null){
            pageNo = "1";
        }
        console.log("pageNo:" + pageNo);


        var tag = $(this).attr("data-tag");
        if (tag == "Previous") {
            //向前，如果当前不是第一页，则向前翻页
            if (pageNo > 1) {
                pageNo--;
                var newurl = changeURLArg(url, "page", pageNo);
                location.href = newurl;//跳转到对应的页面
            }
        } else if (tag == "Next") {
            //向后，如果当前不是最后一页，则翻页
            var pages = $(this).data("page-range");
            if (pageNo == null) {
                var newurl = changeURLArg(url, "page", 2);
                location.href = newurl;//跳转到对应的页面
            } else {
                if (pageNo < pages) {
                    pageNo++;
                    var newurl = changeURLArg(url, "page", pageNo);
                    location.href = newurl;//跳转到对应的页面
                }
            }

        } else {
            var page = $(this).data("page");
            var newurl = changeURLArg(url, "page", page);
            location.href = newurl;//跳转到对应的页面
        }
    });


//按某列排序
    jQuery(".orderBy").click(function () {
        event.preventDefault();//阻止A标签跳转
        var url = location.href;
        var newurl = changeURLArg(url, "sort_by", $(this).data("column"));
        location.href = newurl;//跳转到对应的页面
    });

//排序方向
    jQuery(".sortDirection").click(function (event) {
        event.preventDefault();//阻止A标签跳转
        var url = location.href;
        var sp = $(this).find("span");
        //var css = sp.attr("class");
        if (sp.hasClass("glyphicon-arrow-up")) {
            var newurl = changeURLArg(url, "direction", "desc");
            sp.removeClass("glyphicon-arrow-up");
            sp.addClass("glyphicon-arrow-down");
            location.href = newurl;//跳转到对应的页面
        } else {
            var newurl = changeURLArg(url, "direction", "asc");
            sp.removeClass("glyphicon-arrow-down");
            sp.addClass("glyphicon-arrow-up");
            location.href = newurl;//跳转到对应的页面
        }
    });

//刷新验证码
    jQuery(".next-captcha").click(function (event) {
        event.preventDefault();
        $.getJSON('/refresh-captcha', function (json) {
            // This should update your captcha image src and captcha hidden input
            // debugger;
            var status = json['status'];
            var new_cptch_key = json['new_cptch_key'];
            var new_cptch_image = json['new_cptch_image'];
            var id_captcha_0 = $("#id_reg_captcha_0");
            var img = $(".captcha");
            id_captcha_0.attr("value", new_cptch_key);
            img.attr("src", new_cptch_image);
        });
    });

//ajax验证验证码
    jQuery('.form-control-captcha').blur(function () {
        var key_id = $(this).data('captcha-key')
        var json_data = {
            'response': $(this).val(),
            // 获取输入框和隐藏字段id_captcha_0的数值
            'hashkey': $('#' + key_id).val()
        };

        $.getJSON('/ajax_val_captcha', json_data, function (data) { //ajax发送
            $('#captcha_status').remove();
            if (data['success'] == true) { //status返回1为验证码正确， status返回0为验证码错误， 在输入框的后面写入提示信息
                //alert(data['message']);
            } else {
                //alert(data['message']);
                //$(this).after('<span id="captcha_status" >*' + data['message'] + '</span>')
            }
        });
    });

    /***
     ***   页面跳转类开始
     ***/
    jQuery("#CreateAccount").click(function (event) {
        location.href = "/user/register";
    });

    jQuery(".return-to-cart").click(function () {
        var url = "/quote/show";
        location.href = url;
    });
    /***
     ***   页面跳转类结束
     ***/

//购物车详情
    jQuery(".cart-qty").blur(function (e) {
        var cp_id = $(this).data('cartid');
        var qty = $(this).val();
        imycartModifyCart('set', cp_id, qty, $(this));
    });

    jQuery(".qty-decrease").click(function (e) {
        var cp_id = $(this).data('cartid');
        var current_qty = $("#cartqty-" + cp_id).val();
        if (current_qty <= 1) {
            return;
        } else {
            var qty = current_qty - 1;
            imycartModifyCart('set', cp_id, qty, $(this));
            //$("#cartqty-" + cp_id).val(qty);
        }
    });

    jQuery(".qty-increase").click(function (e) {
        var cp_id = $(this).data('cartid');
        var current_qty = $("#cartqty-" + cp_id).val();
        var qty = parseInt(current_qty) + 1;
        imycartModifyCart('set', cp_id, qty, $(this));
        //$("#cartqty-" + cp_id).val(qty);
    });

    jQuery("[title^=Qty]").blur(function (event) {
        var cartid = $(this).attr("data-cartid");
        var quantity = $(this).val();
        if (quantity == 0) {
            quantity = 1;
            $(this).val(1);
        }
        imycartModifyCart('set', cartid, quantity, $(this));
    });

    jQuery("[title^=Delete]").click(function (event) {
        event.preventDefault();
        var cartid = $(this).attr("data-cartid");
        imycartModifyCart('del', cartid, 0, $(this));
    });

    jQuery("#empty_cart_button").click(function (event) {
        var cartid = $(this).attr("data-cartid");
        imycartModifyCart('clear', cartid, 0, $(this));
    });


    /***
     ***  查看购物车明细页面使用的方法开始 ***
     ***/
    function imycartModifyCart(method, cart_id, quantity, triggerControl) {
        var url = '/cart/modify';
        var cart = new Object();
        cart.method = method;
        cart.cart_id = cart_id;
        cart.quantity = quantity;

        var extraInfo = new Object();
        extraInfo.method = method;
        extraInfo.quantity_origin = quantity;
        extraInfo.cart_id = cart_id;
        imycartAjaxCallWithCallback(url, cart, imycartModifyCartCallback, triggerControl, extraInfo);
    };

    function imycartModifyCartCallback(result, triggerControl, extraInfo) {
        var flag = false;
        if (extraInfo.method == "set") {
            if (result.success == true) {
                $("#price-" + extraInfo.cart_id).text("$" + result.cart_product_total.toFixed(2));
                $("#product-price-" + extraInfo.cart_id).text("$" + result.cart_product_price.toFixed(2));
                $("#cartqty-" + extraInfo.cart_id).val(extraInfo.quantity_origin);
                flag = true;
            } else {
                triggerControl.val(result.origin);
                $("#infoMessage").html(result.message);
                $("#myModal").modal('toggle');
            }

        } else if (extraInfo.method == "del") {
            var tr = triggerControl.parent().parent();
            tr.remove();
            flag = true;
            $(".top-cart-num-link").text(result.cart_item_type_count);
        } else if (extraInfo.method == "clear") {
            //都清空
            flag = true;
            $(".carts-item").remove();
            $(".top-cart-num-link").text(result.cart_item_type_count);
        }

        //更新总金额
        if (flag) {
            imycartUpdateTotalAmount(result.sub_total, result.sub_total);
        }
    };

    function imycartUpdateTotalAmount(totalAmount, totalPrice) {
        //更新商品总价、总运费、总金额
        $("#totalPrice").html("$ " + totalPrice.toFixed(2));
        $("#totalAmount").html("$ " + totalAmount.toFixed(2));
    };
    /***
     ***  查看购物车明细页面使用的方法结束 ***
     ***/
//付款按钮
    jQuery(".order-pay-button").click(function (event) {
        var url = '/cart/payment/' + $(this).data("id");
        location.href = url;
    });


//地址选择
    jQuery(".check-choice-address").click(function () {
        $(".check-address-list").show();
    });


//点击某个地址后，收起下拉菜单，并且填充下面的输入框
//由于动态添加的li，绑定的click事件会失效，因此这里必须用on('click','li>a',function(e))的写法
    jQuery(".check-address-list").on('click', 'li>a', function (e) {
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


//地址添加与修改
    jQuery(".btn-address-submit").click(function () {
        //将按钮设置为不可用
        console.log('Start to update address...')
        $(this).attr('disabled', true);

        //var address_id = $("#select_address_id").val();
        var $form = $("#address-form").data('bootstrapValidator');
        $form.validate();
        var flag = $form.isValid();
        if (!flag) {
            $(this).attr('disabled', false);
            return;
        }
        //alert(flag);


        var submit_method = "dropdown_list";
        if (!($(this).data("submit-method") == "" || $(this).data("submit-method") == null)) {
            submit_method = $(this).data("submit-method");
        }

        var address_id = $("#input_address_id").val();
        var url = "/user/address/opration/";
        if (address_id == "") {
            //说明是新增
            url = url + "add/";
        } else {
            url = url + "modify/";
        }

        $.ajax({
            beforeSend: function (xhr, settings) {
                console.log("Start to set csrftoken.......");
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    console.log("Set the csrf token successful.");
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            cache: false,
            type: "POST",
            url: url,
            data: $('#address-form').serialize(),
            async: false,
            error: function (request) {
                alert('Sorry.An error occured.Please try again.');
            },
            success: function (data) {
                if (data.success == true) {
                    if (submit_method == "dropdown_list") {
                        var address_id = data.address.id;
                        var useage = data.address.useage;
                        var changeFlag = false;
                        $("#ul_address_list li").each(function () {
                            if ($(this).find("a").data("address-id") == address_id) {
                                changeFlag = true;
                                var html = "<a class='address-option' data-address-id='" + address_id + "'>" + useage + "</a>"
                                $(this).html(html);
                                //alert("TODO:Opration success:" + html);
                            }
                        });
                        $("#span_address_selected").text(useage);

                        if (!changeFlag) {
                            //新增的

                            $("#ul_address_list").append("<li><a class='address-option' data-address-id='" + address_id + "'>" + useage + "</a></li>");
                            $("#span_address_selected").text(useage);
                            $(".input-address-id").val(address_id);


                        }
                    } else if (submit_method == "close_self") {
                        //暂时啥都不干
                        location.href = "/user/address/show/"
                    }

                    $(this).attr('disabled', false);
                } else {
                    $(this).attr('disabled', false);
                    if (submit_method == "dropdown_list" || submit_method == "close_self") {
                        $("#infoMessage").html(data.message);
                        $("#myModal").modal('toggle');
                    }
                }

            }
        });
    });

//地址选择的修改
    $("#select_address_id").change(function (e) {
        var address_id = $("#select_address_id").val();
        $.updateAddressForm(address_id);
    });

    $.updateAddressForm = function (address_id) {
        //获取地址的详细信息
        var url = "/user/address/detail/";
        console.log('Reset address.');
        if (address_id == "") {
            //清空下面的列表
            //$("#address-form")[0].reset();
            //重置表单要加个[0],神奇的东东。。。。
            //发现reset方法有个问题，如果input中有value="xx",那么只能还原到xx
            $(':input', '#address-form')
                .not(':button, :submit, :reset, :hidden')
                .val('')
                .removeAttr('checked')
                .removeAttr('selected');
        } else {
            console.log('Set address detail...');
            url = url + address_id;
            console.log('url:' + url);
            $.ajax({
                beforeSend: function (xhr, settings) {
                    console.log("Start to set csrftoken.......");
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        console.log("Set the csrf token successful.");
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                cache: false,
                type: "GET",
                url: url,
                data: null,
                async: false,
                error: function (request) {
                    alert('Sorry.An error occured.Please try again.');
                },
                success: function (data) {
                    if (data.success == true) {
                        for (var key in data.address) {
                            $("#id_" + key).val(data.address[key]); //页面上input必须命名成 "id_字段"的形式
                        }
                    }

                }
            });
        }

        //尝试重置验证状态
        $("#address-form").data('bootstrapValidator').resetForm();
    };

//下单
    jQuery(".btn-place-order").click(function (e) {
        //检查地址有没有选择
        var address_id = $("#input_address_id").val();
        if (address_id > 0) {
            $("#place_order_form").submit();
        } else {
            $("#infoMessage").html("Please choose a shipping address.");
            $("#myModal").modal('toggle');
        }


    });


//取消订单
    jQuery(".order-cancel-button").click(function (event) {
        var url = '/order/cancel';
        var object = new Object();
        object.order_id = $(this).data("id");

        var extraInfo = new Object();
        extraInfo.method = 'cancel';
        extraInfo.order_id = object.order_id;
        imycartAjaxCallWithCallback(url, object, imycartChangeOrderCallBack, $(this), extraInfo)
    });


//用户信息
    jQuery("#changePassword").click(function () {
        if ($("#changePassword").attr('checked')) {
            $(".change-password").hide();
            $("#changePassword").removeAttr('checked');
        }
        else {
            $("#changePassword").attr('checked', 'true');
            $(".change-password").show();
        }
    });


    jQuery(".btn-userinfo-submit").click(function (e) {
        var $form = $("#userInfoForm").data("bootstrapValidator");
        $form.validate();
        if ($form.isValid()) {
            $("#userInfoForm").data("bootstrapValidator").defaultSubmit();
        }

    });

    function imycartChangeOrderCallBack(result, triggerControl, extraInfo) {
        if (extraInfo.method == 'cancel') {
            //删除自己这一行
            var condition = "[title=" + "container_order_" + extraInfo.order_id + "]";
            $(condition).remove();
        }
    };


//把商品添加到愿望清单
    jQuery("#addToWishList").click(
        function (event) {
            event.preventDefault();
            imycartAddProductToWishlist($(this).data("product-id"), $(this), null);
        }
    );
    function imycartAddProductToWishlist(product_id, triggerControl, extraInfo) {
        var url = "/wishlist/add";
        var wish = new Object();
        wish.product_id = product_id;
        imycartAjaxCallWithCallback(url, wish, imycartAddProductToWishlistCallBack, triggerControl, extraInfo);
    };

    function imycartAddProductToWishlistCallBack(result, triggerControl, extraInfo) {
        if (result.success == true) {
            $(".detail-heart").addClass("detail-heart-click");
            $("#infoMessage").html(result.message);
            $("#myModal").modal('toggle');
        } else {
            if (result.message == "needLogin") {
                location.href = "/user/login/?next=" + result.next;
            }
        }
    };

//把商品从愿望清单删除
    jQuery(".remove-from-wishlist").click(
        function (event) {
            event.preventDefault();
            var extraInfo = new Object();
            extraInfo.topDivId = $(this).data("top-div-id");
            imycartRemoveProductFromWishlist($(this).data("wishlistid"), $(this), extraInfo);
        }
    );

    function imycartRemoveProductFromWishlist(wish_id, triggerControl, extraInfo) {
        var url = "/wishlist/remove";
        var wish = new Object();
        wish.id = wish_id;
        var encodedata = $.toJSON(wish);
        imycartAjaxCallWithCallback(url, wish, imycartRemoveProductFromWishlistCallBack, triggerControl, extraInfo);
    };

    function imycartRemoveProductFromWishlistCallBack(result, triggerControl, extraInfo) {
        if (result.success == true) {
            $("#" + extraInfo.topDivId).remove();
        } else {
            $("#infoMessage").html(result.message);
            $("#myModal").modal('toggle');
        }
    };


//选择了商品某个额外属性
    jQuery(".product-attribute-item").click(function () {
        //判断当前点击的是否是无效选项
        if ($(this).parent().hasClass("sku-inavailable") || $(this).parent().hasClass("sku-text-inavailable")) {
            return;
        }

        //判断点击的是已经选中的还是没选中的
        var condition = ".product-attribute-group-selected[title=" + $(this).data("group-code") + "]";

        //本次点击的sku项目的相关信息
        var current_attribute_id = $(this).data("attribute-id");

        if ($(this).parent().hasClass("redborder")) {
            /*  给商品去掉表示选中红框的逻辑 */
            $(this).parent().prevAll().removeClass('redborder');
            $(this).parent().nextAll().removeClass('redborder');
            $(this).parent().removeClass('redborder');
            $(condition).val("");
            $("#current_attrobute_id").val("");
        } else {
            /*  给商品加上表示选中红框的逻辑 */
            $(this).parent().prevAll().removeClass('redborder');
            $(this).parent().nextAll().removeClass('redborder');
            $(this).parent().addClass('redborder');
            $(condition).val($(this).data("attribute-id"));
            $("#current_attrobute_id").val(current_attribute_id);
        }


        var product_to_get = new Object();
        product_to_get.product_id = $(this).data("product-id");

        var attr_list = new Array();
        $(".product-attribute-group-selected").each(function () {
            if ($(this).val() != "") {
                attr_list.push($(this).val());
            }

        });
        product_to_get.attr_list = attr_list;
        var url = '/product/get-product-extra/'
        var encodedata = $.toJSON(product_to_get);
        $.ajax({
            beforeSend: function (xhr, settings) {
                console.log("Start to set csrftoken.......");
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    console.log("Set the csrf token successful.");
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },


            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            url: url,
            data: encodedata,
            success: function (result) {
                if (result.success == true) {
                    $("#product-attribute-id").val(result.message.pa_id);
                    $("#min_order_quantity").text(result.message.min_order_quantity);
                    //确定价格
                    //$("#product-price-main").text("$" + result.message.price.toFixed(2));
                    //现在价格不由SKU决定了

                    //更新显示的大图
                    if (result.message.show_image == true) {
                        $("#product-big-image").attr("jqimg", result.message.image_url);
                        $("#product-big-image").attr("src", result.message.image_url);
                    }
                }
                //不论有没有选择全面，都需要设定可以选择的属性列表
                $(".attr-text").removeClass("sku-text-available");
                $(".attr-text").addClass("sku-text-inavailable");

                $(".attr-img").removeClass("sku-available");
                $(".attr-img").addClass("sku-inavailable");

                var id_and_type = result.available_set;

                if (id_and_type == "all_available") {
                    //全部可选
                    $(".attr-text").removeClass("sku-text-inavailable");
                    $(".attr-text").addClass("sku-text-available");

                    $(".attr-img").removeClass("sku-inavailable");
                    $(".attr-img").addClass("sku-available");
                } else if ($.trim(id_and_type) != "") {
                    var id_list = String(id_and_type).split(",");
                    $.each(id_list, function (index, id) {
                        var tmp = id.split("|")
                        var available_class_name = 'sku-available';
                        var inavailable_class_name = 'sku-inavailable';
                        if (tmp[1] == 'text') {
                            available_class_name = 'sku-text-available';
                            inavailable_class_name = 'sku-text-inavailable';
                        }
                        $("[data-attribute-id=" + tmp[0] + "]").parent().removeClass(inavailable_class_name);
                        $("[data-attribute-id=" + tmp[0] + "]").parent().addClass(available_class_name);
                    });
                }
                //alert('pa_id:' + $("input[name=product-attribute-id]").val());
            },
            error: function (result) {
                alert('Sorry.An error occured.Please try again.');
            }
        });
    });


    jQuery(document).ready(function (e) {
        var item_count = $.cookie('cart_item_type_count') == null ? 0 : $.cookie('cart_item_type_count');
        $(".top-cart-num-link").text(item_count);
    });


    /*
     * url 目标url
     * arg 需要替换的参数名称
     * arg_val 替换后的参数的值
     * return url 参数替换后的url
     */
    function changeURLArg(url, arg, arg_val) {
        if (url.endWith("#")) {
            url = url.replace("#", "");
        }
        var pattern = arg + '=([^&]*)';
        var replaceText = arg + '=' + arg_val;
        if (url.match(pattern)) {
            var tmp = '/(' + arg + '=)([^&]*)/gi';
            tmp = url.replace(eval(tmp), replaceText);
            return tmp;
        } else {
            if (url.match('[\?]')) {
                return url + '&' + replaceText;
            } else {
                return url + '?' + replaceText;
            }
        }
        return url + '\n' + arg + '\n' + arg_val;
    };

    String.prototype.endWith = function (s) {
        if (s == null || s == "" || this.length == 0 || s.length > this.length)
            return false;
        if (this.substring(this.length - s.length) == s)
            return true;
        else
            return false;
        return true;
    };

    String.prototype.startWith = function (s) {
        if (s == null || s == "" || this.length == 0 || s.length > this.length)
            return false;
        if (this.substr(0, s.length) == s)
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
            if (r != null) return unescape(r[2]);
            return null;
        }
    })(jQuery);
});