var app = angular.module('nsApp', ['ngRoute',]);

app.controller('testsCtrl' ,['$scope', '$http', function($scope, $http) {

  $scope.results = null;

  $scope.runAllTests = function(){
    $http.get('/test').success(function(res) {
      $scope.results = res;
    });
  };
}]);
