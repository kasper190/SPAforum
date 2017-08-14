'use strict';

angular.module('core.forum').
    factory('Category', function($resource) {
        var url = '/api/forum/categories/';
        return $resource(url, {}, {
            query: {
                method: 'GET',
                isArray: true,
            }
        });         
    }).
    factory('Subforum', function($resource) {
        var url = '/api/forum/:subforum_slug/';
        return $resource(url, {}, {
            get: {
                method: 'GET',
                params: {"subforum_slug": "@subforum_slug"},
                isArray: false,
                cache: false,
            }
        });          
    }).
    factory('Thread', function(IsAuthenticatedInterceptor, $cookies, $httpParamSerializer, $resource) {
        var url = '/api/forum/:subforum_slug/:thread_slug/';

        var threadGet = {
            url: '/api/forum/:subforum_slug/:thread_slug/',
            method: 'GET',
            params: {
                "subforum_slug": "@subforum_slug",
                "thread_slug": "@thread_slug",
            },
            isArray: false,
            cache: false,
        };

        var threadCreate = {
            url: '/api/forum/thread/create/',
            method: 'POST',
            interceptor: {responseError: IsAuthenticatedInterceptor}
        };  

        var threadUpdate = {
            url: '/api/forum/:subforum_slug/:thread_slug/edit/',
            method: "PUT",
            interceptor: {responseError: IsAuthenticatedInterceptor},
            params: {
                "subforum_slug": "@subforum_slug",
                "thread_slug": "@thread_slug",
            },
        };
        
        var threadDelete = {
            url: '/api/forum/:subforum_slug/:thread_slug/delete/',
            method: "DELETE",
            interceptor: {responseError: IsAuthenticatedInterceptor},
            params: {
                "subforum_slug": "@subforum_slug",
                "thread_slug": "@thread_slug",
            },
        }

        var token = $cookies.get("token");
        if (token) {
            threadCreate["headers"] = {"Authorization": "JWT " + token};
            threadUpdate["headers"] = {"Authorization": "JWT " + token};
            threadDelete["headers"] = {"Authorization": "JWT " + token};
        };

        return $resource(url, {}, {
            get: threadGet,
            create: threadCreate,
            update: threadUpdate,
            delete: threadDelete,
        });  
    });