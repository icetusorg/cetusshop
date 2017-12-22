/* global $ */

$(window).load(function() {
	preloadImagesForCarousel();
	
	$(".carousel").on("aCarouselHasBeenAdjusted", function() {
		sizeChoosing();
		chooseColor();
		adjustIndexesOfCarousel();
	});
	
	$(".carousel.flexible").flexCarousel();
});

function sizeChoosing() {
	$(".size .options").hide();
	
	$(".carousel").off("click").on("click", ".size", function() {
		$(this).clearQueue();
		
		if ($(this).hasClass("shown"))
		{
			$(this).clearQueue().removeClass("shown").find(".options").slideUp(800);
		}
		else
		{
			$(this).clearQueue().addClass("shown").find(".options").slideDown(800);
		}
	});
	
	$(".carousel").on("click", ".option", function() {
		$(this).closest(".size").find(".header .number").html($(this).text());
	});
}

function chooseColor() {
	$(".carousel").on("click", ".choose-color div", function() {
		var img_path = findPathToDirectory($(this).closest(".flex-item").find(".good-image img").attr("src")) + $(this).attr("class") + ".png";
		
		$(this).closest(".flex-item").find(".good-image img").stop().fadeTo("slow", 0, function() {
			$(this).attr("src", img_path);
		}).fadeTo("slow", 1);
	});
}

function findPathToDirectory(path_to_file) {
	return path_to_file.slice(0, path_to_file.lastIndexOf("/") + 1);
}

function adjustIndexesOfCarousel() {
	$(".carousel").each(function() {
		setupIndexesOfCarousel($(this));
	});
	$(".carousel").on("slid.bs.carousel", function() {
		setupIndexesOfCarousel($(this));
	});
}

function setupIndexesOfCarousel(carousel) {
	var total_number = $(carousel).find(".item").length;
	var current_number = $(carousel).find(".item.active").index() + 1;
	
	$(carousel).find(".index").text(String(current_number) + " / " + String(total_number));
}

function preloadImages(images) { 
  for (var i = 0; i < images.length; i++) {
    $("<img />").attr("src", images[i]);
  }
}

function collectImagesForPreloading() {
	var images = [];
	
	$(".carousel .choose-color").each(function() {
		var files = [];
		
		$(this).find("div").each(function() {
			files.push($(this).attr("class"));
		});
		
		var directory = findPathToDirectory($(this).closest(".flex-item").find(".good-image img").attr("src"));
		
		for (var i = 0; i < files.length; i++)
		{
			images.push(directory + files[i] + ".png");
		}
	});
	
	return images;
}

function preloadImagesForCarousel() {
	var images = collectImagesForPreloading();
	
	preloadImages(images);
}