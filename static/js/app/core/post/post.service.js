'use strict';

angular.module('core.post').
    factory('Post', function(IsAuthenticatedInterceptor, $cookies, $httpParamSerializer, $resource) {
        var url = '/api/post/create/';
        
        var postCreate = {
            url: '/api/post/create/',
            method: 'POST',
            interceptor: {responseError: IsAuthenticatedInterceptor}
        };
        
        var postUpdate = {
            url: '/api/post/:id/edit/',
            method: "PUT",
            interceptor: {responseError: IsAuthenticatedInterceptor},
            params: {"id": "@id"},
        };
        
        var postDelete = {
            url: '/api/post/:id/delete/',
            method: "DELETE",
            interceptor: {responseError: IsAuthenticatedInterceptor},
            params: {"id": "@id"},
        };

        var token = $cookies.get("token");
        if (token) {
            postCreate["headers"] = {"Authorization": "JWT " + token};
            postUpdate["headers"] = {"Authorization": "JWT " + token};
            postDelete["headers"] = {"Authorization": "JWT " + token};
        }
        
        return $resource(url, {}, {
            create: postCreate,
            update: postUpdate,
            delete: postDelete,
        });
    }).
    factory('Note', function(IsAuthenticatedInterceptor, $cookies, $httpParamSerializer, $resource) {
        var url = '/api/post/note/create/';
        
        var noteCreate = {
            url: '/api/post/note/create/',
            method: 'POST',
            interceptor: {responseError: IsAuthenticatedInterceptor}
        };

        var noteUpdate = {
            url: '/api/post/note/:id/edit/',
            method: "PUT",
            interceptor: {responseError: IsAuthenticatedInterceptor},
            params: {"id": "@id"},
        };
        
        var noteDelete = {
            url: '/api/post/note/:id/delete/',
            method: "DELETE",
            interceptor: {responseError: IsAuthenticatedInterceptor},
            params: {"id": "@id"},
        };

        var token = $cookies.get("token");
        if (token) {
            noteCreate["headers"] = {"Authorization": "JWT " + token};
            noteUpdate["headers"] = {"Authorization": "JWT " + token};
            noteDelete["headers"] = {"Authorization": "JWT " + token};
        }
        
        return $resource(url, {}, {
            create: noteCreate,
            update: noteUpdate,
            delete: noteDelete,
        });
    });