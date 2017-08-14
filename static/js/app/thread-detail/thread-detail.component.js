'use strict';

angular.module('threadDetail').
    component('threadDetail', {
        template: "<ng-include src='getTemplateUrl()' />",
        controller: function(Note, Post, Message, Thread, $cookies, $filter, $location, $routeParams, $scope, $window) {  
            $scope.loading = true;
            $scope.pageError = false;
            $scope.notFound = false;
            $scope.thread = null;

            $scope.getTemplateUrl = function() {
                if ($scope.loading && $scope.thread == null) {
                    return '/api/templates/loading.html';
                } else if ($scope.notFound) {
                    return '/api/templates/error/404.html';
                } else if ($scope.pageError) {
                    return '/api/templates/error/500.html';
                } else {
                    return '/api/templates/thread-detail.html';
                }
            };


            var subforum_slug = $routeParams.subforum_slug;
            $scope.subforum_slug = subforum_slug;
            var thread_slug = $routeParams.thread_slug;
            
            Thread.get({"subforum_slug": subforum_slug, "thread_slug": thread_slug}, function(data) {
                $scope.thread = data;
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
            $scope.postsPerPage = 10;


            $scope.pageChanged = function(newPage) {
                $location.search('page', newPage).path($location.path());
            };

            $scope.isModerator = function(moderators) {
                if(moderators) {
                    return moderators.includes($scope.currentUser);
                }
            };

            $scope.isAuthor = function(currentUser, author) {
                return currentUser === author;
            };

            $scope.isEdited = function(publish, updated) {
                var publish_filter = $filter('date')(publish, 'medium');
                var updated_filter = $filter('date')(updated, 'medium');
                return  publish_filter !== updated_filter;
            };


            $scope.newContent = {
                threadEdit: '',
                post: '',
                postEdit: '',
                note: '',
                noteEdit: '',
            };


            $scope.threadEdit = false;
            $scope.postEdit = null;
            $scope.postNote = null;
            $scope.noteEdit = null;


            $scope.threadEditError = {};
            $scope.postError = {};
            $scope.postEditError = {};
            $scope.noteError = {};
            $scope.noteEditError = {};


            $scope.$watch(function() {
                if ($scope.newContent.threadEdit) {
                    $scope.threadEditError = {};
                }
                if ($scope.newContent.post) {
                    $scope.postError = {};
                }
                if ($scope.newContent.postEdit) {
                    $scope.postEditError = {};
                }
                if ($scope.newContent.note) {
                    $scope.noteError = {};
                }
                if ($scope.newContent.noteEdit) {
                    $scope.noteEditError = {};
                }
            });


            $scope.threadEditOpen = function() {
                $scope.threadEdit = true;
                $scope.postEdit = null;
                $scope.postNote = null;
                $scope.noteEdit = null;
            };
            $scope.postEditOpen = function(postId) {
                $scope.threadEdit = false;
                $scope.postEdit = postId;
                $scope.postNote = null;
                $scope.noteEdit = null;
                $scope.postEditError = '';
            };
            $scope.postNoteOpen = function(postId) {
                $scope.threadEdit = false;
                $scope.postEdit = null;
                $scope.postNote = postId;
                $scope.noteEdit = null;
                $scope.postEditError = '';
            };
            $scope.noteEditOpen = function(noteId) {
                $scope.threadEdit = false;
                $scope.postEdit = null;
                $scope.postNote = null;
                $scope.noteEdit = noteId;
                $scope.noteEditError = '';
            };
            $scope.cancelEdit = function() {
                $scope.threadEdit = false;
                $scope.postEdit = null;
                $scope.postNote = null;
                $scope.noteEdit = null;
            };

            
            $scope.threadUpdate = function(thread) {
                Thread.update({
                    "subforum_slug": subforum_slug,
                    "thread_slug": thread_slug,
                    title: $scope.newContent.threadEdit,
                    is_open: thread.is_open,
                    type: 'PUT',
                }, function(data) {
                    $scope.thread.title = data.title;
                    $scope.thread.is_open = data.is_open;
                    $scope.threadEdit = false;
                    $scope.threadEditError = {};
                    Message.emit("Thread has been successfully edited.");
                }, function(e_data) {
                    $scope.threadEditError = e_data.data;
                });
            };

            $scope.threadDelete = function(thread) {
                var confirmDelete = $window.confirm('Are you sure you want to delete this Thread?');
                if (confirmDelete) {
                    Thread.delete({
                        "subforum_slug": subforum_slug,
                        "thread_slug": thread_slug,
                    }, function(data) {
                        $location.path('/forum/' + subforum_slug + '/');
                        Message.emit("Thread has been successfully removed.");
                    }, function(e_data) {
                        Message.emit("Operation Thread remove failed.");
                    });
                }
            };

            $scope.postCreate = function() {
                if (!$scope.newContent.post) {
                    $scope.postError.content = ["This field is required."];
                } else {
                    Post.create({
                        user: $scope.currentUserId,
                        thread: $scope.thread.id,
                        content: $scope.newContent.post,
                        type: 'POST',
                    }, function(data) {
                        $scope.thread.posts.push(data);
                        $scope.newContent.post = '';
                        $scope.postError = '';
                        Message.emit("Post has been successfully published.");
                    }, function(e_data) {
                        $scope.postError = e_data.data;
                    });
                 }
            };

            $scope.postUpdate = function(post) {
                if (!$scope.newContent.postEdit) {
                    $scope.postEditError.content = ["This field is required."];
                } else {
                    Post.update({
                        "id": post.id,
                        content: $scope.newContent.postEdit,
                        type: 'PUT',
                    }, function(data) {
                        post.content = data.content;
                        post.updated = data.updated;
                        $scope.postEdit = null;
                        $scope.postEditError = '';
                        Message.emit("Post has been successfully edited.");
                    }, function(e_data) {
                        $scope.postEditError = e_data.data;
                    });
                }
            };

            $scope.postDelete = function(post) {
                var confirmDelete = $window.confirm('Are you sure you want to delete this Post?');
                if (confirmDelete) {
                    Post.delete({
                        "id": post.id
                    }, function(data) {
                        var index = $scope.thread.posts.indexOf(post);
                        $scope.thread.posts.splice(index, 1);
                        Message.emit("Post has been successfully removed.");
                    }, function(e_data) {
                        Message.emit("Operation Post remove failed.");
                    });
                }
            };

            $scope.noteCreate = function(post) {
                if (!$scope.newContent.note) {
                    $scope.noteError.note = ["This field is required."];
                } else {
                    Note.create({
                        user: $scope.currentUserId,
                        post: post.id,
                        note: $scope.newContent.note,
                        type: 'POST',
                    }, function(data) {
                        var post_index = $scope.thread.posts.indexOf(post);
                        $scope.thread.posts[post_index].notes.push(data);
                        $scope.newContent.note = '';
                        $scope.postNote = null;
                        $scope.noteError = '';
                        Message.emit("Note has been successfully published.");
                    }, function(e_data) {
                        $scope.noteError = e_data.data;
                    });
                }
            };
            
            $scope.noteUpdate = function(post, note) {
                if (!$scope.newContent.noteEdit) {
                    $scope.noteEditError.note = ["This field is required."];
                } else {
                    Note.update({
                        "id": note.id,
                        user: $scope.currentUserId,
                        post: post.id,
                        note: $scope.newContent.noteEdit,
                        type: 'PUT',
                    }, function(data) {
                        var post_index = $scope.thread.posts.indexOf(post);
                        var note_index = $scope.thread.posts[post_index].notes.indexOf(note);
                        $scope.thread.posts[post_index].notes[note_index].note = data.note;
                        $scope.thread.posts[post_index].notes[note_index].updated = data.updated;
                        $scope.noteEdit = null;
                        $scope.noteEditError = '';
                        Message.emit("Note has been successfully edited.");
                    }, function(e_data) {
                        $scope.noteEditError = e_data.data;
                    });
                }
            };

            $scope.noteDelete = function(note, post) {
                var confirmDelete = $window.confirm('Are you sure you want to delete this Note?');
                if (confirmDelete) {
                    Note.delete({
                    "id": note.id,
                    }, function(data) {
                        var post_index = $scope.thread.posts.indexOf(post);
                        var note_index = $scope.thread.posts[post_index].notes.indexOf(note);
                        $scope.thread.posts[post_index].notes.splice(note_index, 1);
                        Message.emit("Note has been successfully removed.");
                    }, function(e_data) {
                        Message.emit("Operation Note remove failed.");
                    });
                }
            };
        }
    });