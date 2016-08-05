// 顶部多语言——鼠标移上去显示，移走隐藏
function menuon(){
   $(".menu2").addClass("block");
}
function menuoff(){
   $(".menu2").removeClass("block");
}
/*手机端菜单点击弹出*/
$("#menu-ico").click(function(){
    $(".menu-phone").show();
    $(".wapper").addClass("wapper-move")
    $(".wapper").attr('id','wapper')
    $(".wapper-rgb").show();
})
$(".wapper-rgb").click(function(){
    $(".menu-phone").hide();
    $(".wapper").removeClass("wapper-move")
    $(".wapper-rgb").hide();
})
$(".menu-phone-plus").click(function(){
    var pid = this.getAttribute("data")
    var status = this.getAttribute("status");
    if(status=="close"){
        $("#"+pid).show();
        $(this).attr('status','open');
        $(this).removeClass('glyphicon-plus');
        $(this).addClass('glyphicon-minus');
    }
    if(status=="open"){
        $("#"+pid).hide();
        $(this).attr('status','close');
        $(this).removeClass('glyphicon-minus');
        $(this).addClass('glyphicon-plus');
    }

});
/*手机端向下滚动隐藏顶部菜单*/
$(window).scroll(function(event) {
    var top = $(document).scrollTop();
    var width=$(window).width();
    if(width<769) {
        if (top >100) {
            $(".logo").css("height", "60px");
            $(".menu-phone-ico").css("padding-top", "10px");
            $(".top-middle-right").css("padding-top", "9px");
        }
        else {
            $(".logo").css("height", "80px");
            $(".menu-phone-ico").css("padding-top", "21px");
            $(".top-middle-right").css("padding-top", "19px");
        }
    }
})
//加入购物车飘动效果
$.addcartFlyEfect = function(obj){
    var moveimg=$(".cart-move-img").attr("src");
    var ynums=parseInt($(".top-cart-num").text());
    var addnums=parseInt($(".small-quality").val());
    var wheight=window.screen.height;
    var wwidth=window.screen.width;
    var widthMain=$(".container").width();
    var rights=(wwidth-widthMain)/2;
    var headerh=$('.detail-quality').offset().top; //飘移起点top使用detail-quality同高度
    var star=wheight+headerh;
    var endh=$('.top-cart-num').offset().top+10;
    //var nums=ynums+addnums;
    $(".cart-move").attr("src",moveimg);
    $(".cart-move").show();
    $(".cart-move").animate({
        'top': headerh,
        'right': '54%',
        'width': 120,
        'height': 120
    }, 0);
    $(".cart-move").animate({
        'top': endh,
        'right': rights,
        'width': 30,
        'height': 30
    }, 600);
    $(".cart-move").hide(200);
    setTimeout(function () {}, 1000);
};
//产品颜色色块图片点击加边框
function redborder(obj){
    var clas = obj.getAttribute("class");
    $("."+clas).prevAll().removeClass('redborder');
    $("."+clas).nextAll().removeClass('redborder');
    $("."+clas).addClass('redborder');
}