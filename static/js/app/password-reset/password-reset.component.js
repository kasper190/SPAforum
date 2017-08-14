'use strict';

angular.module('passwordReset').
    component('passwordReset', {
        templateUrl: '/api/templates/password-reset.html',
        controller: function(Message, $cookies, $http, $location, $scope) {
            var passwordResetUrl = '/api/user/password-reset/';
            $scope.email = '';
            $scope.passwordResetError = {};
            var blankError = ["This field may not be blank."];
            $scope.loading = false;
            

            $scope.$watch(function() {
                if ($scope.email && $scope.passwordResetError.email == blankError) {
                    $scope.passwordResetError.email = "";
                } 
            });

            $scope.tokenExists = $cookies.get("token");


            $scope.doPasswordReset = function(email) {
                if (!email) {
                    $scope.passwordResetError.email = blankError;
                }

                if (email) {
                    $scope.loading = true;

                    var reqConfig = {
                        method: "POST",
                        url: passwordResetUrl,
                        data: {
                            email: email
                        },
                        headers: {}
                    };
                    var requestAction = $http(reqConfig);

                    requestAction.success(function(r_data, r_status, r_headers, r_config) {
                        $scope.loading = false;
                        $location.path("/");
                        Message.emit("E-mail with new password has been sent.");
                        // window.location.reload();
                    });
                    requestAction.error(function(e_data, e_status, e_headers, e_config) {
                        $scope.loading = false;
                        $scope.passwordResetError = e_data;
                    });
                }
            };
        }
    });