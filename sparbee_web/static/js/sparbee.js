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
      }).when('/tracktag', {
          templateUrl : 'templates/tracktag',
          controller: 'TrackingController'
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
              $scope.selectedTruck = $scope.trucklist[0];

              $scope.initialize();
            },
            function(errorResponse) {
              alert('Failed to get data from server'
                  + errorResponse.statusText);
            });
      }

      // draws the map on screen.
      $scope.initialize = function() {

        var markers = [];
        $http.get('/api/truck/' + $scope.selectedTruck.id + '/items')
            .then(function(response) {
              locationObjs = response.data;
              $scope.locations = [];

              // from the response objects convert them to an Array of
              // locations
              for(var id in locationObjs) {
                var latlng = new google.maps.LatLng(locationObjs[id].lat, locationObjs[id].lng);
                $scope.locations.push({'id': id,
                  'mac_id': locationObjs[id].mac_id,
                  'location': latlng,
                  'update_time': locationObjs[id].update_time
                });
               }

              if($scope.locations.length > 0){

                // draw the map, center based on first location
                var map = new google.maps.Map(document
                        .getElementById('map_div'), {
                      center : $scope.locations[0].location,
                      mapTypeId : google.maps.MapTypeId.ROADMAP,
                      zoom : 8
                    });

                // draw the markers for the locations
                for( var i=0; i< $scope.locations.length; i++){
                  var marker = new google.maps.Marker({
                    position : $scope.locations[i].location,
                    map : map,
                    title : $scope.locations[i].mac_id
                  });
                }
              }else{
                $('#map_div').html("No location information available");
              }

            }, function(errorResponse) {
              alert('Failed to get map location data from server' + errorResponse.statusText);
            });
      }

      // given lat, lng returns the address.
      // elm: the id of the element that should be used to update the value
      // elm can be changed to a callback later if needed
      $scope.getAddress = function(latlng, elm){
        var geocoder = new google.maps.Geocoder;
        geocoder.geocode({'location': latlng}, function(results, status) {
              if (status === 'OK' && results[1]) {
                $('#' + elm).html(results[1].formatted_address);
              }
        });

      }
      getTruckList();

    } ]);


//given lat, lng returns the address.
// elm: the id of the element that should be used to update the value
// elm can be changed to a callback later if needed
function getAddress(latlng, elm){
  var geocoder = new google.maps.Geocoder;
  geocoder.geocode({'location': latlng}, function(results, status) {
        if (status === 'OK' && results[1]) {
          $('#' + elm).html(results[1].formatted_address);
        }
  });

}

sparbeeApp.controller('TrackingController', ['$scope', '$http', function($scope, $http){

    $scope.getAllTags = function(){
        $http.get('/api/taglist').then(function(response){
            // success case
            try{
                $scope.taglist = response.data;
                $scope.selectedTag = $scope.taglist[0];
                $scope.showTagLocation();

            }catch(err){
                alert(err);
            }
        }, function(errorResponse){
            // error case
            alert('Failed to get tags list from server' + errorResponse.statusText);
        });
    };

    $scope.showTagLocation = function(){
        var lastUpdatedLocation = $scope.selectedTag.location[$scope.selectedTag.location.length - 1];
        if(lastUpdatedLocation != undefined){
            var latlng = new google.maps.LatLng(lastUpdatedLocation.lat, lastUpdatedLocation.lng);
            // draw the map, center based on first location
            var map = new google.maps.Map(document
                    .getElementById('map_div'), {
              center : latlng,
              mapTypeId : google.maps.MapTypeId.ROADMAP,
              zoom : 8
            });

            var marker = new google.maps.Marker({
                position : latlng,
                map : map,
                title : $scope.selectedTag.mac_id
            });

            getAddress(latlng, "lastKnownLocation");
            $scope.updateTime = lastUpdatedLocation.update_time;

        }else{
            $("#map_div").html("No location information available");
            $scope.updateTime = null;
            $("#lastKnownLocation").html("");
        }

    }

    // get all tags from server
    $scope.getAllTags();
}]);
