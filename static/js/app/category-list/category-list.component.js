'use strict';

angular.module('categoryList').
    component('categoryList', {
        template: "<ng-include src='getTemplateUrl()' />",
        controller: function(Category, Message, $scope, $http, $location) {
            $scope.loading = true;
            $scope.pageError = false;
            $scope.notFound = false;
            $scope.categories = null;

            $scope.getTemplateUrl = function() {
                if ($scope.loading && $scope.categories == null) {
                    return '/api/templates/loading.html';
                } else if ($scope.notFound) {
                    return '/api/templates/error/404.html';
                } else if ($scope.pageError) {
                    return '/api/templates/error/500.html';
                } else {
                    return '/api/templates/category-list.html';
                }
            };

            Category.query({}, function(data) {
                $scope.loading = false;
                $scope.categories = data;
            }, function(e_data) {
                $scope.loading = false;
                if (e_data.status == 404) {
                    $scope.notFound = true;
                } else {
                    $scope.pageError = true;
                }
            });
        }
    });