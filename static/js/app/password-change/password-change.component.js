'use strict';

angular.module('passwordChange').
    component('passwordChange', {
        templateUrl: '/api/templates/password-change.html',
        controller: function(Message, $cookies, $http, $location, $routeParams, $rootScope, $scope) {
            var passwordChangeUrl = '/api/user/password-change/';
            $scope.user = {};
            $scope.passwordChangeError = {};
            var blankError = ["This field may not be blank."];


            $scope.tokenExists = $cookies.get("token");
            if ($scope.tokenExists) {
                var token = $cookies.get("token");
            } 


            $scope.$watch(function() {
                if ($scope.user.password && $scope.passwordChangeError.password == blankError) {
                    $scope.passwordChangeError.password = "";
                }
                if ($scope.user.password1 && $scope.passwordChangeError.password1 == blankError) {
                    $scope.passwordChangeError.password1 = "";
                }
                if ($scope.user.password2 && $scope.passwordChangeError.password2 == blankError) {
                    $scope.passwordChangeError.password2 = "";
                }
            });


            $scope.doPasswordChange = function(user) {
                if (!user.password) {
                    $scope.passwordChangeError.password = blankError;
                } 
                if (!user.password1) {
                    $scope.passwordChangeError.password1 = blankError;
                }
                if (!user.password2) {
                    $scope.passwordChangeError.password2 = blankError;
                }
                if (user.password1 && user.password1 != user.password2) {
                    $scope.passwordChangeError.password1 = ["New passwords must match."];
                }

                if (user.password && user.password1 && user.password2) {
                    var reqConfig = {
                        method: "PUT",
                        url: passwordChangeUrl,
                        data: {
                            password: user.password,
                            password1: user.password1,
                            password2: user.password2
                        },
                        headers: {"Authorization": "JWT " + token}
                    };
                    var requestAction = $http(reqConfig);

                    requestAction.success(function(r_data, r_status, r_headers, r_config) {
                            $location.path("/");
                            Message.emit("Password has been successfully updated.");
                            // window.location.reload();
                    });
                    requestAction.error(function(e_data, e_status, e_headers, e_config) {
                            $scope.passwordChangeError = e_data;
                    });
                }
            };
        }
    });