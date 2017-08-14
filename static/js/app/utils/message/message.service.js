'use strict';

angular.module('message').
    factory('Message', function($rootScope) {
        return {
            emit: function(msg) {
                $rootScope.$emit('MessageEmit', {message: msg});
            }
        };
    });