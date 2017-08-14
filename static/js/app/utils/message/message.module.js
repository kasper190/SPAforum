'use strict';

angular.module('message', []).
    run(function($rootScope) {
        $rootScope.$on('MessageEmit', function(event, args) {
            $rootScope.$broadcast('MessageBroadcast', args);
        });
    });