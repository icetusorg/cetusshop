// 手机版菜单栏
$(window).on('load resize', function(event) {
    $(".buttonpush").click(function(event) {
        $(".neirong").addClass('neirong-show');
    });
    $(".neirong-close").click(function(event) {
        $(".neirong").removeClass('neirong-show');
    });
});
jQuery(function ($) {
    $(function () {
        $(".li1").hover(function () {
            $(".index-drop-down").css('display', 'block');
        }, function () {
            $(".index-drop-down").css('display', 'none');
        })
    });
    $(function () {
        $(".index-drop-down").hover(function () {
            $(".index-drop-down").css('display', 'block');
        }, function () {
            $(".index-drop-down").css('display', 'none');
        })
    });

    $(function () {
        $(".li2").hover(function () {
            $(".index-drop-down2").css('display', 'block');
        }, function () {
            $(".index-drop-down2").css('display', 'none');
        })
    });
    $(function () {
        $(".index-drop-down2").hover(function () {
            $(".index-drop-down2").css('display', 'block');
        }, function () {
            $(".index-drop-down2").css('display', 'none');
        })
    });
});