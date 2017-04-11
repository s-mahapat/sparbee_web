/**
 *
 */
var sparbeeApp = angular.module('sparbee', [ 'ngRoute' ]);

sparbeeApp
    .config(function($routeProvider, $locationProvider, $compileProvider) {

      // home
      $routeProvider.when('/home', {
        templateUrl : 'templates/home',
      }).when('/', {
        templateUrl : 'templates/home'
      }).when('/checkout', {
        templateUrl : 'templates/checkout',
        controller : 'checkOutController'
      }).when('/checkin', {
        templateUrl : 'templates/checkin',
        controller : 'checkInController'
      });

      $locationProvider.hashPrefix('');
    });

sparbeeApp.controller('checkOutController', [
    '$scope',
    '$http',
    function($scope, $http) {

      $scope.checkOutList = new Array();
      $scope.save = function() {
        $http({
          method : 'POST',
          url : '/api/checkout',
          data : {
            'trucknumber' : $scope.trucknumber,
            'macid' : $scope.macid
          }
        }).then(
            function(response) {
              $scope.checkOutList.push(response.data);
            },
            function(errorResponse) {
              alert('Failed to save data to server'
                  + errorResponse.statusText);
            });

      }
    } ]);

sparbeeApp.controller('checkInController',
    [
        '$scope',
        '$http',
        function($scope, $http) {

          function getTruckList() {
            $http({
              method : 'GET',
              url : '/api/truck/',
            }).then(
                function(response) {
                  $scope.trucklist = response.data;
                },
                function(errorResponse) {
                  alert('Failed to get data from server'
                      + errorResponse.statusText);
                });
          }

          $scope.initialize = function() {
            console.log('scope init called');
            var map = new google.maps.Map(document
                .getElementById('map_div'), {
              center : {
                lat : 12.971208,
                lng : 77.599121
              },
              zoom : 10
            });
          }

          google.maps.event.addDomListener(window, 'load',
              $scope.initialize);

          getTruckList();

        } ]);
