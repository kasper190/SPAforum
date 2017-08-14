'use strict';

angular.module('registerDetail').
    component('registerDetail', {
        templateUrl: '/api/templates/register-detail.html',
        controller: function(Message, $cookies, $http, $location, $routeParams, $rootScope, $scope) {         
            var registerUrl = '/api/user/register/';
            $scope.user = {};
            $scope.registerError = {};
            var blankError = ["This field may not be blank."];


            $scope.$watch(function() {
                if ($scope.user.username && $scope.registerError.username == blankError) {
                    $scope.registerError.username = "";
                } 
                if ($scope.user.email && $scope.registerError.email == blankError) {
                    $scope.registerError.email = "";
                } 
                if ($scope.user.password && $scope.registerError.password == blankError) {
                    $scope.registerError.password = "";
                }
                if ($scope.user.password2 && $scope.registerError.password2 == blankError) {
                    $scope.registerError.password2 = "";
                }
            });


            if ($cookies.get("token")) {
                Message.emit("You have already registered and logged in.");
            }


            $scope.doRegister = function(user) {
                if (!user.username) {
                    $scope.registerError.username = blankError;
                } 
                if (!user.email) {
                    $scope.registerError.email = blankError;
                } 
                if (!user.password) {
                    $scope.registerError.password = blankError;
                }
                if (!user.password2) {
                    $scope.registerError.password2 = blankError;
                }
                if (user.password && user.password != user.password2) {
                    $scope.registerError.password = ["Passwords must match."];
                }

                if (user.username && user.email && user.password && user.password2) {
                    var reqConfig = {
                        method: "POST",
                        url: registerUrl,
                        data: {
                            username: user.username,
                            email: user.email,
                            password: user.password,
                            password2: user.password2
                        },
                        headers: {}
                    }
                    var requestAction = $http(reqConfig);
                    
                    requestAction.success(function(r_data, r_status, r_headers, r_config) {
                        $cookies.put("token", r_data.token);
                        $cookies.put("username", r_data.username);
                        $cookies.put("id", r_data.id);
                        $location.path("/");
                        // window.location.reload();
                        Message.emit("You have successfully created your account.");
                    });
                    requestAction.error(function(e_data, e_status, e_headers, e_config) {
                        $scope.registerError = e_data; 
                    });
                }
            };
        }
    });