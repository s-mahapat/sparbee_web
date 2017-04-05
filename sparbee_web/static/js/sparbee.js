/**
 * 
 */
var sparbeeApp = angular.module('sparbee', ['ngRoute']);

sparbeeApp.config(function ($routeProvider, $locationProvider, $compileProvider) {

    // home
    $routeProvider.when('/home', {
        templateUrl: 'templates/home'
    }).when('/', {
        templateUrl: 'templates/home'
    }).when('/checkout', {
        templateUrl: 'templates/checkout'
    }).when('/checkin', {
        templateUrl: 'templates/checkin'
    });
    
    $locationProvider.hashPrefix('');
});