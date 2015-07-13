
angular.module('Bidpart', ['ui', 'deal', 'ads'])

	.config(function($interpolateProvider, $httpProvider)
	{
		$interpolateProvider.startSymbol('{!');
		$interpolateProvider.endSymbol('!}');

		$httpProvider.defaults.headers.post['X-CSRFToken'] = $.cookie('csrftoken');
		$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

		$httpProvider.defaults.transformRequest = function(data){
			if (data)
			{
				new_data = {};
				for (var key in data)
				{
					if (data.hasOwnProperty(key))
						new_data[key] = data[key];
				}
				return $.param(new_data);
			}
			else
				return data;
		};
	});


$(document).ready(function() {
	$('[rel="popover"]').popover({

	});
	$('[rel="tooltip"]').tooltip({

	});

	$.fn.select2.defaults['minimumResultsForSearch'] = 10;

	$('select:not([ui-select2])').select2({

	});

    $('#switch_business_profile').on("change", function(e) {
        location.href = '/accounts/switch_business_profile/' + $(this).val() + '/';
    });
    //Deal.init();
});
