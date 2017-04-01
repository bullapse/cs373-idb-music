var app = angular.module('nsApp', []);
app.controller('tracksController', ['$scope', '$sce', function($scope, $sce) {
  $scope.tracks = [
    {spotify_id:"1OcHQQ7A239YbKqKBYw2yw", popularity:44, preview_url:$sce.trustAsResourceUrl("https://p.scdn.co/mp3-preview/4a4a39cb0069e0d304350606f31955d3527d8836?cid=null"),
    image_url:"https://i.scdn.co/image/960b80f3629e54514414559e94692059097f47a1", artist:"Said The Sky", album:"Mountains (feat. Diamond Eyes)",
    name:"Mountains (feat. Diamond Eyes)", duration_ms:268068, explicit:false},
    {spotify_id:"2BvI93upqv44QI4hVTvAC3", popularity:58, preview_url:$sce.trustAsResourceUrl("https://p.scdn.co/mp3-preview/2edce4dd0302c64a1c0cb8a96eb7031bd224bd66?cid=null"),
    image_url:"https://i.scdn.co/image/c782f73e268db268125b5d5cfd3b9899169f6fc0", artist:"Sweater Beats",album:"Hey Ya",
    name:"Hey Ya", duration_ms:187595, explicit:false},
    {spotify_id:"53wXk7sMOnvkdAcEpGzu8W", popularity:51, preview_url:$sce.trustAsResourceUrl("https://p.scdn.co/mp3-preview/2a1eecc5f246f25d86cfe14d1c90ff51f96a8d86?cid=null"),
    image_url:"https://i.scdn.co/image/73aa446c9253a71d384df1c75d92af1d058ee014", artist:"Sweater Beats", album:"Did You Wrong (feat. MAX) - FRND Remix",
    name:"Did You Wrong (feat. MAX) - FRND Remix", duration_ms:165405, explicit:false}];
  }]);

app.controller('artistsController', ['$scope', function($scope) {
  $scope.artists = [
    {spotify_id:"4LZ4De2MoO3lP6QaNCfvcu", popularity:53, 'followers': {'href': null, 'total': 21473},
    image_url:"https://i.scdn.co/image/a5b87b9272ad5a829a6be5619bec6f782b599632", name:"Said The Sky"},
    {spotify_id:"62Jfwxon19ZOT9eSL6bvtY", popularity:51, 'followers': {'href': null, 'total': 24162},
    image_url:"https://i.scdn.co/image/0f5923463e1d98879567b12d409dd24a7c9cbdf6", name:"Sweater Beats"},
    {spotify_id:"2cFrymmkijnjDg9SS92EPM", popularity:74, 'followers': {'href': null, 'total': 367811},
    image_url:"https://i.scdn.co/image/92c55f8da5e3bafafef2192ebfcb027d1711a5c9", name:"Blackbear"}];
  }]);


app.controller('albumsController', ['$scope', function($scope) {
  $scope.albums = [
    {spotify_id:"6S0sbdQmuF3IhNRcMkuQK3", popularity:63, release_date: "2016-02-17",
    image_url:"https://i.scdn.co/image/4f66562a98fa019c88ef8b56e721f67fb43632a8", artist:"Blackbear",
    name:"Help"},
    {spotify_id:"4w0aS3VhSU7QHEN4zfpvHv", popularity:33, release_date: "2015-12-18",
    image_url:"https://i.scdn.co/image/960b80f3629e54514414559e94692059097f47a1", artist:"Said The Sky",
    name:"Mountains (feat. Diamond Eyes)"},
    {spotify_id:"41B7cBcRZDSE62bo0eoBTW", popularity:46, release_date: "2016-10-14",
    image_url:"https://i.scdn.co/image/3bfe3babb6af8e426c9d3d8032545479097da6aa", artist:"3LAU",
    name:"Fire"}];
  }]);
