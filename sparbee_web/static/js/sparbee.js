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

sparbeeApp.controller('checkInController', [
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

      // draws the map on screen.
      $scope.initialize = function() {

        var markers = [];
        $http.get('/api/truck/1/items')
            .then(function(response) {
            }, function(errorResponse) {
            });
        var myLatlng = new google.maps.LatLng(12.971208, 77.599121);
        var map = new google.maps.Map(document
            .getElementById('map_div'), {
          center : myLatlng,
          mapTypeId : google.maps.MapTypeId.ROADMAP,
          zoom : 10
        });

        var marker = new google.maps.Marker({
          position : myLatlng,
          map : map,
          title : 'Location'
        });
      }

      $scope.getMarkers = function() {

      }

      getTruckList();

    } ]);
