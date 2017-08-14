'use strict';

angular.module('spaforum').
    config(function($locationProvider, $resourceProvider, $routeProvider) {
        $locationProvider.html5Mode({
            enabled: true
        });
        
        $resourceProvider.defaults.stripTrailingSlashes = false;
        $routeProvider.
            when('/', {
                template: '<category-list></category-list>'
            }).
            when("/login", {
                template: "<login-detail></login-detail>"
            }).
            when("/register", {
                template: "<register-detail></register-detail>"
            }).
            when("/user/password-change", {
                template: "<password-change></password-change>"
            }).
            when("/user/password-reset", {
                template: "<password-reset></password-reset>"
            }).
            when("/user/:username", {
                template: "<user-detail></user-detail>"
            }).
            when('/forum/:subforum_slug', {
                template: '<subforum-detail></subforum-detail>',
            }).
            when('/forum/:subforum_slug/:thread_slug', {
                template: '<thread-detail></thread-detail>',
            }).
            otherwise({
                templateUrl: '/api/templates/error/404.html'
            });
    }); 