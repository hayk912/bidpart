jQuery(document).ready(function($) {
	$('#ad-detail-image-slider').royalSlider({
		fullscreen: {
			enabled: true,
			nativeFS: false
		},
		autoPlay: {
			enabled: true,
			pauseOnHover: true
		},
		video: {
			autoHideArrows:false
		},
		transitionType: 'fade',
		autoScaleSlider: true,
		autoScaleSliderWidth: 300,
		autoScaleSliderHeight: 185,
		imageScalePadding:1,
		loop: false,
		numImagesToPreload:4,
		arrowsNavAutohide: true,
		arrowsNavHideOnTouch: true,
		keyboardNavEnabled: true
	});
});
