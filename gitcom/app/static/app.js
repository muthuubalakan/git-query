var gitCom = angular.module("gitCom", ['ngRoute']);

gitCom.config(function($routeProvider) {
	$routeProvider
	.when('/', {
		templateUrl: 'static/templates/home.html'
	})
	.when('/admin', {
		templateUrl: 'static/templates/admin.html'
	})
});
