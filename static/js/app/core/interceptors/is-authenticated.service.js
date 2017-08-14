'use strict';

angular.module('core.interceptors').
    factory("IsAuthenticatedInterceptor", function($cookies, $location) {
        return function(response) {
            if (response.status == 401) {
                var currentPath = $location.path();
                if (currentPath == "/login") {
                    $location.path("/login");
                } else {
                    $location.path("/login").search("next", currentPath);
                }
            }
        };
    })