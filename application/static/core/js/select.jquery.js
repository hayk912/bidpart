
(function($) {

	$.fn.selectReplacement = function(method) {

		var changeVal = function(event) {
			event.preventDefault();

			var $this = $(this);
			var $btn_group = $this.closest('.btn-group');
			var $select = $btn_group.prev();
			var $option = $('[value="'+$this.data('value')+'"]', $select);
			var $btn_text = $('a.dropdown-toggle .text', $btn_group);

			$select.children().attr('selected', false);
			$option.attr('selected', true);
			$btn_text.text($option.text());

			$select.trigger('change');
		};

		var filterItem = function($item, query) {
			var $a_tag = $item.children();

			return !!$a_tag.text().toLowerCase().indexOf(query.toLowerCase());
		};

		var search = function(event) {
			var $this = $(this);
			var query = $this.val();
			var $items = $this.parent().children('li');

			$items.each(function(){
				var $item = $(this);

				if (filterItem($item, query))
				{
					$item.css('display', 'none');
				}
				else
				{
					$item.css('display', 'block');
				}
			});
		};

		var searchClick = function(event) {
			return false;
		};

		var btnClick = function(event) {
			var $btn = $(this);
			var $input = $btn.next().children('input');

			$input.val('');
			$input.trigger('keyup');
			setTimeout(function(){ $input.focus(); }, 0);
		};
		
		return this.each(function(){
			var $select = $(this);
			var $selected = $(':selected', $select);
			var $btn_group = $('<div class="btn-group"></div>');
			var $btn = $('<a class="btn dropdown-toggle dropdown-arrow" data-toggle="dropdown"><span class="text"></span></a>');
			var $menu = $('<ul class="dropdown-menu"></ul>');
			//var $search_field = $('<input type="search" />');

			$('option', $select).each(function(){
				var $this = $(this);
				var $item = $('<li><a data-value="'+$(this).attr('value')+'" href="#">'+$this.text()+'</a></li>');

				$menu.append($item);
			});

			$('.text', $btn).text($selected.text());

			$menu.delegate('li a', 'click', changeVal);
			//$search_field.on('keyup', search);
			//$search_field.on('click', searchClick);
			$btn.on('click', btnClick);
			$btn.addClass($select.attr('class'));

			$btn_group.css('display', 'inline-block');
			//$search_field.css('margin', '3px 20px');
			$menu.css('overflow-y', 'auto');
			$menu.css('overflow-x', 'hidden');
			$select.css('display', 'none');
			$menu.css('max-height', 22 * 10);
			//$menu.prepend($search_field);

			$btn_group.append($btn);
			$btn_group.append($menu);
			
			template = angular.element($btn_group.html());
			$select.after($btn_group);
		});
	};

})(jQuery);

jQuery(document).ready(function(){
	setTimeout(function(){
		//jQuery('select:not([ui-select2])').selectReplacement();
	}, 0);
});
