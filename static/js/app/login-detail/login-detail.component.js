'use strict';

angular.module('loginDetail').
    component('loginDetail', {
        templateUrl: '/api/templates/login-detail.html',
        controller: function(Message, $cookies, $http, $location, $routeParams, $rootScope, $scope) {
            var loginUrl = '/api/user/login/';
            $scope.loginError = {};
            $scope.user = {};

            $scope.$watch(function() {
                if ($scope.user.username) {
                    $scope.loginError.username = "";
                }
                if ($scope.user.password) {
                    $scope.loginError.password = "";
                }
            });

            var tokenExists = $cookies.get("token");
            if (tokenExists) {
                $cookies.remove("token");
                $scope.user = {
                    username: $cookies.get("username")
                };
                window.location.reload();
            }

            $scope.doLogin = function(user) {
                if (!user.username) {
                    $scope.loginError.username = ["This field may not be blank."];
                } 
                if (!user.password) {
                    $scope.loginError.password = ["This field is required."];
                }

                if (user.username && user.password) {
                    var reqConfig = {
                        method: "POST",
                        url: loginUrl,
                        data: {
                            username: user.username,
                            password: user.password
                        },
                        cache: false,
                        headers: {}
                    };
                    var requestAction = $http(reqConfig);
                    
                    requestAction.success(function(r_data, r_status, r_headers, r_config) {
                        $cookies.put("token", r_data.token);
                        $cookies.put("username", r_data.username);
                        $cookies.put("id", r_data.id);

                        var next = $location.search().next;
                        if (next) {
                            $location.path(next);
                        } else {
                            $location.path("/");
                        }

                        // window.location.reload();
                        Message.emit("You have logged in successfully.");
                    });
                    requestAction.error(function(e_data, e_status, e_headers, e_config) {
                        $scope.loginError = e_data;
                    });
                }
            };   
        }
    });