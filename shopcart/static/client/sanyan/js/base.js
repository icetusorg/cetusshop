function tabs(tabId, tabNum) {
    $(tabId + " .tab li").removeClass("curr");
    $(tabId + " .tab li").eq(tabNum).addClass("curr");
    $(tabId + " .tabcon").hide();
    $(tabId + " .tabcon").eq(tabNum).show()
}
function preview(img) {
    $("#preview .jqzoom img").attr("src", $(img).attr("src"));
    $("#preview .jqzoom img").attr("jqimg", $(img).attr("bimg"))
}
$(function () {
    $(".jqzoom").jqueryzoom({xzoom: 480, yzoom: 480})
});
$(function () {
    var tempLength = 0;
    var viewNum = 5;
    var moveNum = 2;
    var moveTime = 300;
    var scrollDiv = $(".spec-scroll .items ul");
    var scrollItems = $(".spec-scroll .items ul li");
    var moveLength = scrollItems.eq(0).width() * moveNum;
    var countLength = (scrollItems.length - viewNum) * scrollItems.eq(0).width();
    $(".spec-scroll .next").bind("click", function () {
        if (tempLength < countLength) {
            if ((countLength - tempLength) > moveLength) {
                scrollDiv.animate({left: "-=" + moveLength + "px"}, moveTime);
                tempLength += moveLength
            } else {
                scrollDiv.animate({left: "-=" + (countLength - tempLength) + "px"}, moveTime);
                tempLength += (countLength - tempLength)
            }
        }
    });
    $(".spec-scroll .prev").bind("click", function () {
        if (tempLength > 0) {
            if (tempLength > moveLength) {
                scrollDiv.animate({left: "+=" + moveLength + "px"}, moveTime);
                tempLength -= moveLength
            } else {
                scrollDiv.animate({left: "+=" + tempLength + "px"}, moveTime);
                tempLength = 0
            }
        }
    })
});