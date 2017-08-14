'use strict';

angular.module('spaforumNav').
    component('spaforumNav', {
        templateUrl: '/api/templates/spaforum-nav.html',
        controller: function(Message, $cookies, $http, $scope, $location) {         
            var descriptionsUrl = '/api/forum/descriptions/';
            
            $http({
                method: "GET",
                url: descriptionsUrl
            }).then(function successCallback(response) {
                $scope.forum = response.data;
                document.title = $scope.forum.forum_name
            }, function errorCallback(response) {
                $scope.forum.forum_name = 'Forum';
                $scope.forum.description = '';
            });

            $scope.isActive = function (viewLocation) { 
                if (viewLocation === '/forum' && $location.path() === '/') {
                    return true;
                }
                return $location.path().startsWith(viewLocation);
            };

            $scope.$watch(function() {
                var token = $cookies.get("token");
                if (token) {
                    $scope.currentUser = $cookies.get("username");
                } else {
                    $scope.currentUser = '';                    
                }
            });

            $scope.userLogut = function() {
                $cookies.remove("token");
                $cookies.remove("username");
                $cookies.remove("id");
                $location.path('/');
                window.location.reload();
                // Message.emit("You have logged out successfully.");
            };
        }
    });