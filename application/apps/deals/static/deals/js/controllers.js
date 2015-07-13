
angular.module('deal', ['ngResource'])

    .factory('Deal', function($resource)
    {
		return $resource('/deals/create');
    })

	.controller('DealController', ['$scope', 'Deal', '$http', function($scope, Deal, $http)
	{
		$scope.valid = false;
		$scope.errors = [];
		$scope.show_bid = false;

		if (window.location.hash) {
			$(window.location.hash).modal();
		}

		var didSave = function(response, getReponseHeaders)
		{
			$scope.errors = [];
			$scope.valid = true;
		};

        var didUpdateSave = function(response, getReponseHeaders)
        {
            $scope.errors = [];
            $scope.valid = true;
            setTimeout(function() {
                window.location = window.location.href.split('#')[0] + '#deal-' + $scope.id;
				window.location.reload();
            }, 1000);
        };

		var didFail = function(response, getReponseHeaders)
		{
			$scope.errors = [];
			var data = response.data ? response.data : response;
			angular.forEach(data.errors, function(error, key){
				$scope.errors[key] = error;
			});
		};

		$scope.submitDealCreate = function(){
			var deal = new Deal();

            deal.ad = $scope.ad;
			deal.bid = $scope.bid;
			deal.amount = $scope.amount;

			deal.$save(didSave, didFail);
		};

		$scope.submitDealUpdate = function(){
			var data = {action:$scope.action};
			if ($scope.action == 'cancel')
				data['cancel_reason'] = $scope.cancel_reason;
			else if ($scope.action == 'complete') {
				data['price'] = $scope.price;
				data['amount'] = $scope.amount;
			}

			$http.post('/deals/update/'+$scope.id+'/', data)
				.success(didUpdateSave)
				.error(didFail);
		};
	}]
);
