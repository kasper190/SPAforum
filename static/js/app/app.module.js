'user strict';

angular.module('spaforum', [
    // external
    'angularUtils.directives.dirPagination',
    'monospaced.elastic',
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    // internal
    'categoryList',
    'loginDetail',
    'message',
    'passwordChange',
    'passwordReset',
    'registerDetail',
    'subforumDetail',
    'spaforumNav',
    'threadDetail',
    'userDetail',
]);