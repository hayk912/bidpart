
(function($, undefined) {
	var ad_list_sidebar = {

		$el : null,
		$last_clicked : null,

		init : function() {
			$('#main-container').delegate('#id_business_domain', 'change', function(){
				if (ad_list_sidebar.supports_history_api()) {
					ad_list_sidebar.$last_clicked = $(this);
					history.pushState(null, null, '/' + $(this).val() + '/');
					$.get('/' + $(this).val() + '/', ad_list_sidebar.did_get_content, 'html');
				}
				else
				{
					window.location.href = '/' + $(this).val() + '/';
				}

			});

			if (ad_list_sidebar.supports_history_api())
			{
				ad_list_sidebar.$el = $('#ad-list-sidebar');

				ad_list_sidebar.$el.css('position', 'relative');
				ad_list_sidebar.$el.css('height', ad_list_sidebar.$el.children('ul').outerHeight());
				ad_list_sidebar.$el.children('ul').css('position', 'absolute');

				ad_list_sidebar.$el.delegate(':not(.dropdown-item) a', 'click', function(){
					history.pushState(null, null, $(this).attr('href'));
					ad_list_sidebar.$last_clicked = $(this);

					$.get($(this).attr('href'), ad_list_sidebar.did_get_content, 'html');
					return false;
				});
			}
		},

		supports_history_api : function() {
			return !!(window.history && history.pushState);
		},

		did_get_content : function(data){
			var $new_html = $(data);
			var $old_ul = ad_list_sidebar.$el.children('ul');
			var $new_ul = $('#ad-list-sidebar ul', $new_html);

			$('select', $new_ul).select2();

			if ($old_ul.data('field') == $new_ul.data('field'))
			{
				if (ad_list_sidebar.$last_clicked.is('select'))
				{
					$new_ul.css('position', 'absolute');
					$old_ul.css('position', 'absolute');

					ad_list_sidebar.$el.append($new_ul);

					ad_list_sidebar.anim_replace($old_ul, $new_ul);
				}
				else
				{
					$old_ul.remove();
					ad_list_sidebar.$el.html($new_ul);
				}

				ad_list_sidebar.place_ad_list($new_html);
			}
			else
			{
				$new_ul.css('position', 'absolute');
				$old_ul.css('position', 'absolute');

				ad_list_sidebar.$el.append($new_ul);

				if (ad_list_sidebar.$last_clicked.hasClass('back')) {
					ad_list_sidebar.anim_back($old_ul, $new_ul);
				}
				else if (ad_list_sidebar.$last_clicked.is('select')) {
					ad_list_sidebar.anim_back($old_ul, $new_ul);
				}
				else {
					ad_list_sidebar.anim_fwd($old_ul, $new_ul);
				}

				ad_list_sidebar.place_ad_list($new_html);
			}
		},

		place_ad_list : function($new_html){
			var $ad_list = $('#ad-list');
			var $new_ad_list_content = $('#ad-list', $new_html).children();

			$ad_list.html($new_ad_list_content);
			$ad_list.scope().update($ad_list);
		},

		anim_replace : function($old_ul, $new_ul){

			ad_list_sidebar.$el.animate({'height': $new_ul.outerHeight()});
			$('li.list-item a', $new_ul).css('height', 0);

			$('li.list-item a', $old_ul).animate({'height': 0});
			$('li.list-item a', $new_ul).animate({'height': 30}, function(){
				$old_ul.remove();
			});
		},

		anim_back : function($old_ul, $new_ul){
			$new_ul.css('left', -220);

			$old_ul.animate({
				'left': 220
			}, function(){
				$(this).remove();
			});

			$new_ul.animate({
				'left': 0
			}, function(){

			});

			ad_list_sidebar.$el.animate({
				'height': $new_ul.outerHeight()
			}, function(){

			});
		},

		anim_fwd : function($old_ul, $new_ul){
			$new_ul.css('left', 220);

			$old_ul.animate({
				'left': -220
			}, function(){
				$(this).remove();
			});

			$new_ul.animate({
				'left': 0
			}, function(){

			});

			ad_list_sidebar.$el.animate({
				'height': $new_ul.outerHeight()
			}, function(){

			});
		}
	};

	window.ad_list_sidebar = ad_list_sidebar;
}(window.jQuery));
