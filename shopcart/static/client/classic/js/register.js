	$("#email").blur(function(){email();});//验证邮箱格式方法
	$("#password").blur(function(){password();}); //验证密码方法
	$("#confirmPassword").blur(function(){confirmPassword();});//验证确认密码方法
	
	//点击提交按钮事件
	$("#submitAccount").click(function(){
		            if(email()&&password()&& confirmPassword()){ //先验证输入是否通过	
										  	 
					event.preventDefault();
					var url = "${ctxPath}/User/Register.json";
					var user = new Object();
					user.email = $("#email").val();
					user.password = $("#password").val();
					var encodedata = $.toJSON(user);
					$.ajax({
					  type: 'POST',
					  contentType : 'application/json',
					  dataType: 'json',
					  url: url,
					  data: encodedata,
					  success: function(result){
						  	if(result.success=="true"){   
								    $("#infoMessage").html("Register success" + result.data);	
								    $("input[type=reset]").trigger("click");  //清空输入框内容
					                emptyInput();						  	  //输入框变回输入前颜色
									
				                	setTimeout(function () {location.href = "${ctxPath}/User/Login.htm";}, 3000); //页面输出成功消息，等待3秒执行下面
							}else{
								    $("input[type=reset]").trigger("click");  //清空输入框内容
					                emptyInput();						  	  //输入框变回输入前颜色
									$("#infoMessage").html("Register faild" + result.data);
							}				
					  },
					  error: function(result){
					    	$("#infoMessage").html("Register faild" + result.success);
					  }
				});	
		}
	});	

	
	//清楚输入框颜色状态	
	function emptyInput(){
		$("#regEmail").removeClass("has-success");
		$("#regPassword").removeClass("has-success");
		$("#regConfirmPassword").removeClass("has-success");
		$("#iEmail").hide(300);
		$("#iPassword").hide(300);
		$("#iConfirmPassword").hide(300);
	}
	//验证邮箱格式
    function email(){
		 var patter = /\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/;  
		 var valu = $("#email").val();

    if (!patter.test(valu)) {  
       $("#regEmail").removeClass("has-success")
       $("#regEmail").addClass("has-error","has-feedback");
	   $("#iEmail").removeClass("glyphicon-ok");
	   $("#iEmail").addClass("glyphicon-remove");
	   $("#iEmail").show(300);
	   $("#emailMessage").text("* Required Fields");
    }else{ 
	   $("#regEmail").removeClass("has-error");
	   $("#regEmail").addClass("has-success","has-feedback");
	   $("#iEmail").removeClass("glyphicon-remove");
	    $("#iEmail").addClass("glyphicon-ok");
	   $("#iEmail").show(100);
	   $("#emailMessage").text("");
        return true;      
	}
	}
	//验证密码样式
	function password(){
		var strLength = $("#password").val().length;
		if(strLength>20 || strLength<6){			
		$("#regPassword").removeClass("has-success")
        $("#regPassword").addClass("has-error","has-feedback");
	    $("#ipassword").removeClass("glyphicon-ok");
	    $("#iPassword").addClass("glyphicon-remove");
		$("#iPassword").show(300);
	    $("#passwordMessage").text("Password must be 6-20 characters");
		}else{ 
	    $("#regPassword").removeClass("has-error");
	    $("#regPassword").addClass("has-success","has-feedback");
	    $("#iPassword").removeClass("glyphicon-remove");
	    $("#iPassword").addClass("glyphicon-ok");
	    $("#iPassword").show(100);
	    $("#passwordMessage").text("");
        return true;      
	    }
	}		
    
	//验证确认密码样式
	function confirmPassword(){
        var password = $("#password").val();
		var confirmPassword = $("#confirmPassword").val();
		var strLength = confirmPassword.length;
		if(password == confirmPassword && strLength<21 && strLength>5){
		$("#regConfirmPassword").removeClass("has-error");
	    $("#regConfirmPassword").addClass("has-success","has-feedback");
	    $("#iConfirmPassword").removeClass("glyphicon-remove");
	    $("#iConfirmPassword").addClass("glyphicon-ok");
	    $("#iConfirmPassword").show(100);
	    $("#confirmPasswordMessage").text("");
        return true;			
		}else{ 
	    $("#regConfirmPassword").removeClass("has-success")
        $("#regConfirmPassword").addClass("has-error","has-feedback");
	    $("#iConfirmPassword").removeClass("glyphicon-ok");
	    $("#iConfirmPassword").addClass("glyphicon-remove");
		$("#iConfirmPassword").show(300);
	    $("#confirmPasswordMessage").text("Please make sure your passwords match.");    
		}
	}
