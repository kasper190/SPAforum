'use strict';

angular.module('message').
    component('message', {
        templateUrl: '/api/templates/message.html',
        controller: function($scope, $timeout) {        
            $scope.message = '';
            $scope.showMessage = false;

            $scope.$on('MessageBroadcast', function(event, args) {
                $scope.message = args.message;
                $scope.showMessage = true;
                $timeout(function() {
                    $scope.showMessage = false;
                    // $scope.message = '';
                }, 3000 );
            });
        }
    });