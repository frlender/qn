var qn = angular.module('qn',[]);

qn.factory('csv2arr',['$http','$q',function($http){
  return function(url,delim='\t'){
      var deferred = $q.defer();
			$http.get(url).success(function(data){
        var lines = S(data).replaceAll('\r','').trim().split('\n')
        var content = _.map(lines,function(line){
          return S(line).trim().split(delim);
        });
				deferred.resolve(content);
			});
			return deferred.promise;
  }
}])
.factory('loadGeneList',['$http','$q',function($http){
    return function(url){
      var deferred = $q.defer();
      $http.get(url).success(function(data){
				deferred.resolve(data);
			});
			return deferred.promise;
    }
}]);
