angular.module('ads', [])
    .directive('buttonsRadio', function() {
        return {
            restrict: 'A',
            scope: {
                model: '=ngModel'
            },
            link: function(scope, elem, attrs) {
                elem.find('button').on('click', function() {
                    var val = $(this).val();
                    scope.$apply(function() {
                        scope.model = val;
                    });
                });

                scope.$watch('model', function(newVal) {
                    elem.find('button').removeClass('active');
                    if (newVal) {
                        elem.find('button[value="' + newVal + '"]').addClass('active');
                    }
                    else {
                        elem.find('button[value=""]').addClass('active');
                    }

                });
            }
        };
    })
    .directive('bidpartCommission', ['$timeout', '$http', function($timeout, $http) {
        return {
            restrict: 'A',
            scope: {
                price: '=price',
                currency: '=currency',
                disabled: '=disabled',
                bidpart_commission: '@'
            },
            link: function($scope, $elem, $attrs) {
                var commission_url = '/ad_api/get_provision/';
                var get_commission_timout;

                function get_commission()
                {
                    if (!$scope.disabled) {
                        $timeout.cancel(get_commission_timout);
                        get_commission_timout = $timeout(function() {
                            $http.get(commission_url, {params: {price: $scope.price, currency: $scope.currency}})
                                .success(function(data) {
                                    $scope.bidpart_commission = data.commission;
                                });
                        }, 500);
                    }
                }

                $scope.$watch('price', get_commission);
                $scope.$watch('currency', get_commission);
                $scope.$watch('disabled', get_commission);
            }
        }
    }])
    .directive('uploader', [function(){
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function($scope, $element, $attrs){
                $element.on('change', function(){
                    var name = 'iframe-' + Math.random().toString(36).substring(2);
                    var $iframe = jQuery('<iframe src="javascript:false;"></iframe>').attr({name:name, id:name});
                    var $form = jQuery('<form method="POST" enctype="multipart/form-data"></form>').attr({action:$attrs['uploader'], target:name});
                    var $csrf = jQuery('<input type="text">').attr({name:'csrfmiddlewaretoken', value:$.cookie('csrftoken')});
                    var $requested_with = jQuery('<input type="text">').attr({name:'X-Requested-With', value:'IFrame'});
                    var $placeholder = jQuery('<div class="progress progress-info progress-striped active"><div class="bar" style="width: 100%"></div></div>');
                    var $body = jQuery('body');

                    $form.hide();
                    $iframe.hide();

                    $element.after($placeholder);
                    $form.append($element);
                    $form.append($csrf);
                    $form.append($requested_with);

                    $body.append($iframe);
                    $body.append($form);

                    $iframe.on('load', function(){
                        var doc = this.contentWindow ? this.contentWindow.document : (this.contentDocument ? this.contentDocument : this.document);
                        var root = doc.documentElement ? doc.documentElement : doc.body;
                        var $textarea = jQuery(root).find('textarea');
                        var data = jQuery.parseJSON($textarea.val());
                        var status = $textarea.data('status');

                        $scope.$emit('uploader.complete', {data:data, status:status, sender:$attrs['ngModel']});

                        $placeholder.after($element);
                        $placeholder.remove();
                        $iframe.remove();
                        $form.remove();
                        $csrf.remove();
                    });

                    $form.submit();
                });
            }
        }
    }])

    .directive('bpHref', [function(){
        return {
            restrict: 'A',
            link: function($scope, $element, $attrs){
                $element.on('click', function(){
                    window.location.href = $attrs['bpHref'];
                });
            }
        }
    }])

    .controller('AdList', ['$scope', '$compile', function($scope, $compile)
    {
        $scope.update = function($new_html) {
            $compile($new_html)($scope);
        }
    }])

    .controller('HeaderFilterController', ['$scope', function($scope)
    {
        $scope.filterOpen = false;
        $scope.filters = {};

        $scope.submit = function()
        {
            var url_args = [];
            var params = {};
            var url;
            var url_params = ['business_domain', 'product_category', 'product_type'];

            for (var i in url_params)
            {
                if (url_params.hasOwnProperty(i))
                {
                    if ($scope.fields[url_params[i]].value)
                        url_args.push($scope.fields[url_params[i]].value);
                }
            }

            for (var param in $scope.fields)
            {
                if ($scope.fields.hasOwnProperty(param))
                {
                    if (url_params.indexOf(param) == -1 && $scope.fields[param].value)
                        params[param] = $scope.fields[param].value;
                }
            }

            url = '/' + url_args.join('/');
            params = $.param(params);

            if (params)
                params = '?' + params;

            console.log(url + params);
            window.location.assign(url + params);
        };
    }])

    .controller('AdFormController', ['$scope', '$http', '$timeout', function($scope, $http, $timeout)
    {
        $scope.product_type_fields_url = '';

        var fields_url = '/ad_api/product_type_fields/$1/$2';
        var types_url = '/ad_api/product_types/$1/';

        function get_uploaded(choices, newValue)
        {
            var temp = [];
            angular.forEach(choices, function(choice){
                if (newValue.indexOf(parseInt(choice.key)) != -1 || newValue.indexOf(choice.key.toString()) != -1 || newValue.indexOf(choice.key) != -1)
                {
                    temp.push(choice.value);
                }
            });

            return temp;
        }

        $scope.$watch('fields.price.value', function(newVal) {
            if (newVal === '') {
                $scope.quote_wanted = false;
            }
            else {
                $scope.quote_wanted = !newVal;
            }
        });

        function upload_complete(field, key, value)
        {
            if (!$scope.fields[field].choices)
                $scope.fields[field]['choices'] = [];

            $scope.fields[field].choices.push({
                key: key,
                value: value
            });

            if (!$scope.fields[field].value)
                $scope.fields[field]['value'] = [];

            $scope.fields[field].value.push(key);
        }

        $scope.remove_file = function($event, model){
            var key = angular.element($event.target).data('key');
            if ($scope.fields[model].value[key])
                $scope.fields[model].value.splice(key, 1);
        };


        $scope.$watch('fields.images.value', function(newValue, oldValue){
            $scope.uploaded_images = get_uploaded($scope.fields.images.choices, newValue);
        }, 'true');

        $scope.$watch('fields.files.value', function(newValue, oldValue){
            $scope.uploaded_files = get_uploaded($scope.fields.files.choices, newValue);
        }, 'true');

        $scope.$on('uploader.complete', function(event, response){
            if (response.data.errors){
                if (response.sender == 'file_to_upload')
                    $scope.fields.files['errors'] = response.data.errors;
                else
                    $scope.fields.images['errors'] = response.data.errors;

                $scope.$digest();
                return;
            }

            if (response.sender == 'file_to_upload')
                upload_complete('files', response.data['pk'].toString(), response.data['filename']);
            else if (response.sender == 'image_to_upload')
                upload_complete('images', response.data['pk'].toString(), response.data['list_thumb']);

            $scope.$digest();
        });

        $scope.$watch('fields.product_type.value', function(){
            if ($scope.fields.product_type.value) {
                $scope.product_type_fields_url = fields_url
                    .replace('$1', $scope.fields.product_type.value)
                    .replace('$2', $scope.fields.is_request.value ? 1 : '');
            }
            else {
                $scope.product_type_fields_url = undefined;
            }
        });
        $scope.$watch('fields.is_request.value', function(){
            if ($scope.fields.product_type.value) {
                $scope.product_type_fields_url = fields_url
                    .replace('$1', $scope.fields.product_type.value)
                    .replace('$2', $scope.fields.is_request.value ? 1 : '');
            }
        });

        $scope.$watch('fields.product_category.value', function(newValue, oldValue){
            if (oldValue != newValue)
            {
                if (!newValue) {
                    newValue = 0;
                }
                var url = types_url.replace('$1', newValue);
                $scope.fields.product_type.loading = true;

                $http({method:'GET', url:url}).success(function(data){
                    $scope.fields.product_type.choices = data;
                    $scope.fields.product_type.loading = false;
                });
            }
        });
    }]);
