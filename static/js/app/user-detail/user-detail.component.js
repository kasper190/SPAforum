'use strict';

angular.module('userDetail').
    component('userDetail', {
        templateUrl: '/api/templates/user-detail.html',
        controller: function($cookies, $http, $routeParams, $scope) {  
            var username = $routeParams.username;
            var userUrl = '/api/user/' + username + '/';

            $http.get(userUrl).then(function successCallback(response) {
                $scope.user = response.data;
            });

            if ($cookies.get("token")) {
                $scope.currentUser = $cookies.get("username");
            }

            $scope.is_Owner = function(currentUser, owner) {
                return currentUser === owner;
            };
        }
    });