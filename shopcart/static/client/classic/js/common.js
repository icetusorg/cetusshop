jQuery(document).ready(function() {
    "use strict";
		/* menu */
    jQuery("#nav > li").hover(function() {
        var el = jQuery(this).find(".level0-wrapper");
        el.hide();
        el.css("left", "0");
        el.stop(true, true).delay(150).fadeIn(300, "easeOutCubic");
    }, function() {
        jQuery(this).find(".level0-wrapper").stop(true, true).delay(300).fadeOut(300, "easeInCubic");
    });
    var scrolled = false;

    jQuery("#nav li.level0.drop-menu").mouseover(function() {
        if (jQuery(window).width() >= 740) {
            jQuery(this).children('ul.level1').fadeIn(100);
        }
        return false;
    }).mouseleave(function() {
        if (jQuery(window).width() >= 740) {
            jQuery(this).children('ul.level1').fadeOut(100);
        }
        return false;
    });
    jQuery("#nav li.level0.drop-menu li").mouseover(function() {
        if (jQuery(window).width() >= 740) {
            jQuery(this).children('ul').css({
                top: 0,
                left: "165px"
            });
            var offset = jQuery(this).offset();
            if (offset && (jQuery(window).width() < offset.left + 325)) {
                jQuery(this).children('ul').removeClass("right-sub");
                jQuery(this).children('ul').addClass("left-sub");
                jQuery(this).children('ul').css({
                    top: 0,
                    left: "-167px"
                });
            } else {
                jQuery(this).children('ul').removeClass("left-sub");
                jQuery(this).children('ul').addClass("right-sub");
            }
            jQuery(this).children('ul').fadeIn(100);
        }
    }).mouseleave(function() {
        if (jQuery(window).width() >= 740) {
            jQuery(this).children('ul').fadeOut(100);
        }
    });

	/* best-seller-slider */
    jQuery("#best-seller-slider .slider-items").owlCarousel({
        items: 6, //10 items above 1000px browser width
        itemsDesktop: [1024, 4], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 3], // 3 items betweem 900px and 601px
        itemsTablet: [600, 2], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false
    });

	/* bag-seller-slider */
    jQuery("#bag-seller-slider .slider-items").owlCarousel({
        items: 3, //10 items above 1000px browser width
        itemsDesktop: [1024, 4], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 3], // 3 items betweem 900px and 601px
        itemsTablet: [600, 2], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false
    });
	/* bag-seller-slider */
    jQuery("#bag-seller-slider1 .slider-items").owlCarousel({
        items: 3, //10 items above 1000px browser width
        itemsDesktop: [1024, 4], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 3], // 3 items betweem 900px and 601px
        itemsTablet: [600, 2], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false
    });
	/* featured-seller-slider */
    jQuery("#featured-slider .slider-items").owlCarousel({
        items: 4, //10 items above 1000px browser width
        itemsDesktop: [1024, 4], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 3], // 3 items betweem 900px and 601px
        itemsTablet: [600, 2], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false
    });
	/* special-slider */
    jQuery("#special-slider .slider-items").owlCarousel({
        items: 1, //10 items above 1000px browser width
        itemsDesktop: [1024, 1], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 1], // 3 items betweem 900px and 601px
        itemsTablet: [600, 2], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false

    });
	/* recommend-slider */
    jQuery("#recommend-slider .slider-items").owlCarousel({
        items: 6, //10 items above 1000px browser width
        itemsDesktop: [1024, 4], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 3], // 3 items betweem 900px and 601px
        itemsTablet: [600, 2], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false
    });
	/* brand-logo-slider */
    jQuery("#brand-logo-slider .slider-items").owlCarousel({
        autoplay: true,
        items: 6, //10 items above 1000px browser width
        itemsDesktop: [1024, 4], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 3], // 3 items betweem 900px and 601px
        itemsTablet: [600, 2], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false
    });
	/* category-desc-slider */
    jQuery("#category-desc-slider .slider-items").owlCarousel({
        autoplay: true,
        items: 1, //10 items above 1000px browser width
        itemsDesktop: [1024, 1], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 1], // 3 items betweem 900px and 601px
        itemsTablet: [600, 1], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false
    });
	/* more-views-slider */
    jQuery("#more-views-slider .slider-items").owlCarousel({
        autoplay: true,
        items: 3, //10 items above 1000px browser width
        itemsDesktop: [1024, 4], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 3], // 3 items betweem 900px and 601px
        itemsTablet: [600, 2], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false
    });
	/* related-products-slider */
    jQuery("#related-products-slider .slider-items").owlCarousel({
        items: 4, //10 items above 1000px browser width
        itemsDesktop: [1024, 4], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 3], // 3 items betweem 900px and 601px
        itemsTablet: [600, 2], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false
    });
	/* upsell-products-slider */
    jQuery("#upsell-products-slider .slider-items").owlCarousel({
        items: 4, //10 items above 1000px browser width
        itemsDesktop: [1024, 4], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 3], // 3 items betweem 900px and 601px
        itemsTablet: [600, 2], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false
    });
	/* crosssel-products-slider */
    jQuery("#crosssel-products-slider .slider-items").owlCarousel({
        items: 5, //10 items above 1000px browser width
        itemsDesktop: [1024, 4], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 3], // 3 items betweem 900px and 601px
        itemsTablet: [600, 2], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false
    });
	/* more-views-slider */
    jQuery("#more-views-slider .slider-items").owlCarousel({
        autoplay: true,
        items: 3, //10 items above 1000px browser width
        itemsDesktop: [1024, 4], //5 items between 1024px and 901px
        itemsDesktopSmall: [900, 3], // 3 items betweem 900px and 601px
        itemsTablet: [600, 2], //2 items between 600 and 0;
        itemsMobile: [320, 1],
        navigation: true,
        navigationText: ["<a class=\"flex-prev\"></a>", "<a class=\"flex-next\"></a>"],
        slideSpeed: 500,
        pagination: false
    });
    jQuery(document).ready(function(jQuery) {
        jQuery("#mobile-menu").mobileMenu({
            MenuWidth: 250,
            SlideSpeed: 300,
            WindowsMaxWidth: 767,
            PagePush: true,
            FromLeft: true,
            Overlay: true,
            CollapseMenu: true,
            ClassName: "mobile-menu"
        });
    });
    jQuery(function(jQuery) {
        "use strict";
        jQuery(".collapsed-block .expander").click(function(e) {
            var collapse_content_selector = jQuery(this).attr("href");
            var expander = jQuery(this);
            if (!jQuery(collapse_content_selector).hasClass("open")) expander.addClass("open").html("&minus;");
            else expander.removeClass("open").html("+");
            if (!jQuery(collapse_content_selector).hasClass("open")) jQuery(collapse_content_selector).addClass("open").slideDown("normal");
            else jQuery(collapse_content_selector).removeClass("open").slideUp("normal");
            e.preventDefault()
        })
    });
    /*========== Left Nav ===========*/

    jQuery(document).ready(function() {

        //increase/ decrease product qunatity buttons +/- in cart.html table
        if (jQuery('.subDropdown')[0]) {
            jQuery('.subDropdown').click(function() {
                jQuery(this).toggleClass('plus');
                jQuery(this).toggleClass('minus');
                jQuery(this).parent().find('ul').slideToggle();
            });
        }

    });

    /*=============End Left Nav=============*/


});


jQuery()
    .ready(function() {
        (function(element) {
            jQueryelement = jQuery(element);
            itemNav = jQuery('.item-nav', jQueryelement);
            itemContent = jQuery('.pdt-content', jQueryelement);
            btn_loadmore = jQuery('.btn-loadmore', jQueryelement);
            ajax_url = "http://www.magikcommerce.com/producttabs/index/ajax";
            catids = '39';
            label_allready = 'All Ready';
            label_loading = 'Loading ...';

            function setAnimate(el) {
                jQuery_items = jQuery('.item-animate', el);
                jQuery('.btn-loadmore', el).fadeOut('fast');
                jQuery_items.each(function(i) {
                    jQuery(this).attr("style", "-webkit-animation-delay:" + i * 300 + "ms;" + "-moz-animation-delay:" + i * 300 + "ms;" + "-o-animation-delay:" + i * 300 + "ms;" + "animation-delay:" + i * 300 + "ms;");
                    if (i == jQuery_items.size() - 1) {
                        jQuery(".pdt-list", el).addClass("play");
                        jQuery('.btn-loadmore', el).fadeIn(i * 0.3);
                    }
                });
            }
            setAnimate(jQuery('.tab-content-actived', jQueryelement));

            itemNav.click(function() {
                var jQuerythis = jQuery(this);
                if (jQuerythis.hasClass('tab-nav-actived')) return false;
                itemNav.removeClass('tab-nav-actived');
                jQuerythis.addClass('tab-nav-actived');
                var itemActive = '.' + jQuerythis.attr('data-href');
                itemContent.removeClass('tab-content-actived');
                jQuery(".pdt-list").removeClass("play");
                jQuery(".pdt-list .item").removeAttr('style');
                jQuery('.item', jQuery(itemActive, jQueryelement)).addClass('item-animate').removeClass('animated');
                jQuery(itemActive, jQueryelement).addClass('tab-content-actived');

                contentLoading = jQuery('.content-loading', jQuery(itemActive, jQueryelement));
                isLoaded = jQuery(itemActive, jQueryelement).hasClass('is-loaded');
                if (!isLoaded && !jQuery(itemActive, jQueryelement).hasClass('is-loading')) {
                    jQuery(itemActive, jQueryelement).addClass('is-loading');
                    contentLoading.show();
                    pdt_type = jQuerythis.attr('data-type');
                    catid = jQuerythis.attr('data-catid');
                    orderby = jQuerythis.attr('data-orderby');
                    jQuery.ajax({
                        type: 'POST',
                        url: ajax_url,
                        data: {
                            numberstart: 0,
                            catid: catid,
                            orderby: orderby,
                            catids: catids,
                            pdt_type: pdt_type
                        },
                        success: function(result) {
                            if (result.listProducts != '') {
                                jQuery('.pdt-list', jQuery(itemActive, jQueryelement)).html(result.listProducts);
                                jQuery(itemActive, jQueryelement).addClass('is-loaded').removeClass('is-loading');
                                contentLoading.remove();
                                setAnimate(jQuery(itemActive, jQueryelement));
                                setResult(jQuery(itemActive, jQueryelement));
                            }
                        },
                        dataType: 'json'
                    });
                } else {
                    jQuery('.item', itemContent).removeAttr('style');
                    setAnimate(jQuery(itemActive, jQueryelement));
                }
            });

            function setResult(content) {
                jQuery('.btn-loadmore', content).removeClass('loading');
                itemDisplay = jQuery('.item', content).length;
                jQuery('.btn-loadmore', content).parent('.pdt-loadmore').attr('data-start', itemDisplay);
                total = jQuery('.btn-loadmore', content).parent('.pdt-loadmore').attr('data-all');
                loadnum = jQuery('.btn-loadmore', content).parent('.pdt-loadmore').attr('data-loadnum');
                if (itemDisplay < total) {
                    jQuery('.load-number', content).attr('data-total', (total - itemDisplay));
                    if ((total - itemDisplay) < loadnum) {
                        jQuery('.load-number', content).attr('data-more', (total - itemDisplay));
                    }
                }
                if (itemDisplay == total) {
                    jQuery('.load-number', content).css({
                        display: 'none'
                    });
                    jQuery('.btn-loadmore', content).addClass('loaded');
                    jQuery('.load-text', content).text(label_allready);
                } else {
                    jQuery('.load-text', content).text(label_loadmore);
                }
            }
            btn_loadmore.on('click.loadmore', function() {
                var jQuerythis = jQuery(this);
                itemActive = '.' + jQuerythis.parent('.pdt-loadmore').attr('data-href');
                jQuery(".pdt-list").removeClass("play");
                jQuery(".pdt-list .item").removeAttr('style');
                jQuery('.item', jQuery(itemActive, jQueryelement)).addClass('animated').removeClass('item-animate');
                if (jQuerythis.hasClass('loaded') || jQuerythis.hasClass('loading')) {
                    return false;
                } else {
                    jQuerythis.addClass('loading');
                    jQuery('.load-text', jQuerythis).text(label_loading);
                    numberstart = jQuerythis.parent('.pdt-loadmore').attr('data-start');
                    catid = jQuerythis.parent('.pdt-loadmore').attr('data-catid');
                    pdt_type = jQuerythis.parent('.pdt-loadmore').attr('data-type');
                    orderby = jQuerythis.parent('.pdt-loadmore').attr('data-orderby');
                    jQuery.ajax({
                        type: 'POST',
                        url: ajax_url,
                        data: {
                            numberstart: numberstart,
                            catid: catid,
                            orderby: orderby,
                            catids: catids,
                            pdt_type: pdt_type
                        },
                        success: function(result) {
                            if (result.listProducts != '') {
                                animateFrom = jQuery('.item', jQuery(itemActive, jQueryelement)).size();
                                jQuery(result.listProducts).insertAfter(jQuery('.item', jQuery(itemActive, jQueryelement)).nextAll().last());
                                setAnimate(jQuery(itemActive, jQueryelement));
                                setResult(jQuery(itemActive, jQueryelement));
                            }
                        },
                        dataType: 'json'
                    });
                }
                return false;
            });
        })('#magik_producttabs1');
    });
//]]>


var isTouchDevice = ('ontouchstart' in window) || (navigator.msMaxTouchPoints > 0);
jQuery(window).on("load", function() {

    if (isTouchDevice) {
        jQuery('#nav a.level-top').click(function(e) {
            jQueryt = jQuery(this);
            jQueryparent = jQueryt.parent();
            if (jQueryparent.hasClass('parent')) {
                if (!jQueryt.hasClass('menu-ready')) {
                    jQuery('#nav a.level-top').removeClass('menu-ready');
                    jQueryt.addClass('menu-ready');
                    return false;
                } else {
                    jQueryt.removeClass('menu-ready');
                }
            }
        });
    }
    //on load
    jQuery().UItoTop();


}); //end: on load

//]]>

jQuery(window).scroll(function() {
    if (jQuery(this).scrollTop() > 1) {
        jQuery('nav').addClass("sticky");
    } else {
        jQuery('nav').removeClass("sticky");
    }
});



/*To top*/
(function(jQuery) {
    jQuery.fn.UItoTop = function(options) {

        var defaults = {
            text: '',
            min: 200,
            inDelay: 600,
            outDelay: 400,
            containerID: 'toTop',
            containerHoverID: 'toTopHover',
            scrollSpeed: 1200,
            easingType: 'linear'
        };

        var settings = jQuery.extend(defaults, options);
        var containerIDhash = '#' + settings.containerID;
        var containerHoverIDHash = '#' + settings.containerHoverID;

        jQuery('body').append('<a href="#" id="' + settings.containerID + '">' + settings.text + '</a>');
        jQuery(containerIDhash).hide().click(function() {
                jQuery('html, body').animate({
                    scrollTop: 0
                }, settings.scrollSpeed, settings.easingType);
                jQuery('#' + settings.containerHoverID, this).stop().animate({
                    'opacity': 0
                }, settings.inDelay, settings.easingType);
                return false;
            })
            .prepend('<span id="' + settings.containerHoverID + '"></span>')
            .hover(function() {
                jQuery(containerHoverIDHash, this).stop().animate({
                    'opacity': 1
                }, 600, 'linear');
            }, function() {
                jQuery(containerHoverIDHash, this).stop().animate({
                    'opacity': 0
                }, 700, 'linear');
            });

        jQuery(window).scroll(function() {
            var sd = jQuery(window).scrollTop();
            if (typeof document.body.style.maxHeight === "undefined") {
                jQuery(containerIDhash).css({
                    'position': 'absolute',
                    'top': jQuery(window).scrollTop() + jQuery(window).height() - 50
                });
            }
            if (sd > settings.min)
                jQuery(containerIDhash).fadeIn(settings.inDelay);
            else
                jQuery(containerIDhash).fadeOut(settings.Outdelay);
        });

    };
})(jQuery);


/*-----购物车数量，保存在cookie中-----*/


function setCartItems(){
	var items =  $.cookie("cartItems");
	if(items){
		$("#topItemCount").html(items);
	}else{
		$("#topItemCount").html("0");
	}
}

function getQueryString(name) {//取URL参数  你要得到userid 就传userid
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
    }



/*-------- End Cart js -------------------*/


jQuery.extend(jQuery.easing, {
    easeInCubic: function(x, t, b, c, d) {
        return c * (t /= d) * t * t + b;
    },
    easeOutCubic: function(x, t, b, c, d) {
        return c * ((t = t / d - 1) * t * t + 1) + b;
    },
});

(function(jQuery) {
    jQuery.fn.extend({
        accordion: function() {
            return this.each(function() {

                function activate(el, effect) {
                    jQuery(el).siblings(panelSelector)[(effect || activationEffect)](((effect == "show") ? activationEffectSpeed : false), function() {
                        jQuery(el).parents().show();
                    });
                }
            });
        }
    });
})(jQuery);

jQuery(function(jQuery) {
    jQuery('.accordion').accordion();
    jQuery('.accordion').each(function(index) {
        var activeItems = jQuery(this).find('li.active');
        activeItems.each(function(i) {
            jQuery(this).children('ul').css('display', 'block');
            if (i == activeItems.length - 1) {
                jQuery(this).addClass("current");
            }
        });
    });

});

/*-------- End Nav js -------------------*/
