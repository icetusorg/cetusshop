/**
 * Created by sq200 on 2017-06-28.
 */
// 手机版菜单栏
$(window).on('load resize', function (event) {
    $(".buttonpush").click(function (event) {
        $(".neirong").addClass('neirong-show');
    });
    $(".neirong-close").click(function (event) {
        $(".neirong").removeClass('neirong-show');
    });
});
jQuery(function ($) {
    $(".index-search").click(function () {
        if ($(this).parent().hasClass("opened")) {
            $(this).parent().parent().next(".header-search").slideUp();
            $(this).parent().removeClass("opened");
        } else {
            $(this).parent().parent().next(".header-search").slideDown();
            $(this).parent().addClass("opened");
        }
    });

    var Cwidth = document.documentElement.clientWidth;
    if ( Cwidth > 992) {
        $(".product-list-list-img").hover(function () {
            $(this).parent().parent().children(".product-list-list-title").slideDown();
        }, function () {
            $(this).parent().parent().children(".product-list-list-title").slideUp();
        });
    }
});
