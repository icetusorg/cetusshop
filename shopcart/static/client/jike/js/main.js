jQuery(function ($) {
    $(".plus3").click(function () {
        if ($(this).parent().hasClass("opened")) {
            $(this).parent().parent().parent().parent().next(".header-search").slideUp();
            $(this).parent().removeClass("opened");
        } else {
            $(this).parent().parent().parent().parent().next(".header-search").slideDown();
            $(this).parent().addClass("opened");
        }
    });
});
/**
 * Created by sq200 on 2017-01-11.
 */
// logo显示导航
$(window).on('load resize', function(event) {
    if ($(window).width()>768) {
        $(".gf-header .gf-pnav").show();
        $(".gf-logo h1").mouseenter(function(event) {
            $(".gf-header .gf-pnav").hide();
            $(".gf-logo .gf-public").slideDown("fast");
        });
        $(".gf-logo").mouseleave(function(event) {
            //$(window).bind("scroll",function(){
            // $(".gf-logo .gf-pnav").hide();
            $(".gf-logo .gf-public").slideUp("fast", function(){
                $(".gf-header .gf-pnav").show();
            });
        });

    }else{
        $(".gf-header .gf-pnav").hide();
    }
});
// 手机版菜单栏
$(window).on('load resize', function(event) {
    $(".buttonpush").click(function(event) {
        $(".neirong").addClass('neirong-show');
    });
    $(".neirong-close").click(function(event) {
        $(".neirong").removeClass('neirong-show');
    });
});


// zoom

function mouseimg(obj){
    var pid=obj.getAttribute("id");
    if($(document).width()>768){
        $("#"+pid).addClass("avatars");
    }
}

function mouseout(obj){
    var pid=obj.getAttribute("id");
    if($(document).width()>768){
        $("#"+pid).removeClass("avatars");
    }
}
