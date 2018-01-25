/**
 * main.js
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Copyright 2014, Codrops
 * http://www.codrops.com
 */
jQuery(function ($) {
    $(".plus3").click(function () {
        if ($(this).parent().hasClass("opened")) {
            $(this).parent().parent().next(".header-search-down").slideUp();
            $(this).parent().removeClass("opened");
        } else {
            $(this).parent().parent().next(".header-search-down").slideDown();
            $(this).parent().addClass("opened");
        }
    });
});
// 手机版菜单栏
$(window).on('load resize', function (event) {
    $(".buttonpush").click(function (event) {
        $(".neirong").addClass('neirong-show');
    });
    $(".neirong-close").click(function (event) {
        $(".neirong").removeClass('neirong-show');
    });
});
