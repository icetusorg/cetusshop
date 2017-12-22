$(function(){
	/*modal 下拉选择*/
	$("#selectOption li").click(function(obj){
		var option=$(this).text();
		$(".selectInput").text(option);
	});
})