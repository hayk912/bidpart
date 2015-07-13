
(function($, undefined) {
	window.init_frontpage_slider = function()
	{
		$('#frontpage-slider').royalSlider({
			autoPlay: {
				enabled: true,
				pauseOnHover: true
			},
			transitionType: 'move',
			autoHeight:true,
			loop: true,
			arrowsNavAutohide: false,
			arrowsNavHideOnTouch: false,
			keyboardNavEnabled: true
		});
	};
}(window.jQuery));

