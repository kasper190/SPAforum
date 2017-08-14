'use strict';

angular.module('subforumDetail').
    component('subforumDetail', {
        template: "<ng-include src='getTemplateUrl()' />",
        controller: function(Message, Subforum, Thread, $cookies, $routeParams, $scope, $location) {
            $scope.loading = true;
            $scope.pageError = false;
            $scope.notFound = false;
            $scope.subforum = null;

            $scope.getTemplateUrl = function() {
                if ($scope.loading && $scope.subforum == null) {
                    return '/api/templates/loading.html';
                } else if ($scope.notFound) {
                    return '/api/templates/error/404.html';
                } else if ($scope.pageError) {
                    return '/api/templates/error/500.html';
                } else {
                    return '/api/templates/subforum-detail.html';
                }
            };


            var subforum_slug = $routeParams.subforum_slug;
            Subforum.get({"subforum_slug": subforum_slug}, function(data) {
                $scope.loading = false;
                $scope.subforum = data;
            }, function(e_data) {
                $scope.loading = false;
                if (e_data.status == 404) {
                    $scope.notFound = true;
                } else {
                    $scope.pageError = true;
                }
            });
            

            if ($cookies.get("token")) {
                $scope.currentUser = $cookies.get("username");
                $scope.currentUserId = $cookies.get("id");
            }


            var pageUrl = $location.search().page;
            if (pageUrl) {
                $scope.currentPage = pageUrl;
            } else {
                $scope.currentPage = 1;
            }
            $scope.threadsPerPage = 20;


            $scope.pageChanged = function(newPage) {
                $location.search('page', newPage).path($location.path());
            };


            $scope.newThread = {
                title: '',
                post: '',
            };
            $scope.threadError = {};
            
            $scope.$watch(function() {
                if ($scope.newThread.title){
                    $scope.threadError.thread = '';
                }
                if ($scope.newThread.post){
                    $scope.threadError.post = '';
                }
            });

            $scope.cancelThread = function() {
                $scope.newThread.title = '';
                $scope.newThread.post = '';
            };


            $scope.threadCreate = function() {
                if (!$scope.newThread.title) {
                    $scope.threadError.thread = ["This field is required."];
                }
                if (!$scope.newThread.post) {
                    $scope.threadError.post = ["This field is required."];
                } else {
                    Thread.create({
                        subforum: $scope.subforum.id,
                        user: $scope.currentUserId,
                        title: $scope.newThread.title,
                        post: $scope.newThread.post,
                        type: 'POST',
                    }, function(data) {
                        $scope.show = false
                        $scope.threadError.thread = ''
                        $scope.threadError.post = ''
                        $location.path('forum/' + subforum_slug + '/' + data.thread_slug)
                        Message.emit("Thread has been successfully published.")
                    }, function(e_data) {
                        $scope.threadError = e_data.data
                    });
                }
            };
        }
    });