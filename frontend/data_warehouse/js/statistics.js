(function () {
  'use strict';

  var app = angular.module("app", ['chart.js', 'ui.bootstrap', '720kb.datepicker']);

  app.config(function (ChartJsProvider) {
    // Configure all charts
    ChartJsProvider.setOptions({
      colors: ['#97BBCD', '#DCDCDC', '#F7464A', '#46BFBD', '#FDB45C', '#949FB1', '#4D5360']
    });
    // Configure all doughnut charts
    /*
    ChartJsProvider.setOptions('doughnut', {
      cutoutPercentage: 60
    });
    ChartJsProvider.setOptions('bubble', {
      tooltips: { enabled: false }
    });
    */
  });  

  app.controller('ChartController', ['$scope', '$http', '$attrs', '$element', function ($scope, $http, $attrs, $element) {
    $scope.labels = [];
    $scope.series = ['Pakete'];
    $scope.data   = [[]];    
    $scope.type_options = ["line", "pie", "bar"];
    $scope.type     = $scope.type_options[0];
    $scope.options  = { legend: { display: true } };    
    $scope.all_time = true

    $scope.dataLoaded = false

    $scope.from_date = new Date(0)
    $scope.from_date_obj = new Date(0)   
    $scope.from_date_nice = "-" 

    $scope.to_date = new Date()
    $scope.to_date_obj = new Date()
    $scope.to_date_nice = ""

    $scope.no_data_available = false

    $scope.information_options = {
        "sizes"         : {"url" : "size", "type" : 1},
        "vehicles"      : {"url" : "location_vehicle_current", "type" : 1},
        "avg_delivery"  : {"url" : "average_delivery/day", "type" : 2},
        "location_day"  : {"url" : "location_vehicle_current/day", "type" : 3},
        "location_hour" : {"url" : "location_vehicle_current/hour", "type" : 3},
        "avg_weight_day":{"url" : "average_weight/day", "type" : 2},
        "registrations_day":{"url" : "registration/day", "type" : 2},
        "registrations_hour":{"url" : "registration/hour", "type" : 2},
        "addresses"     : {"url" : "location_address_current", "type" : 1,
        "filterfun": function (text, zahl) {
            return text != "registert" && text != "delivery" && zahl >= 5
        }},
        "city_send"     : {"url" : "sender_city", "type" : 1,
        "filterfun" : function (text, zahl) {
            return zahl > 100
        }},
        "city_receive"     : {"url" : "receiver_city", "type" : 1,
        "filterfun" : function (text, zahl) {
            return zahl > 100
        }}
    }

    var getDateString = function(obj) {
      return obj.getDate() + "." + (obj.getMonth()+1) + "." + obj.getFullYear()
    }
    
    $scope.$watch('from_date', function (value) {
      try {
       $scope.from_date_obj = new Date(value);
       $scope.from_date_nice = getDateString($scope.from_date_obj);
       $scope.setData();
      } catch(e) {
        console.log(e)
      }
    });

    $scope.$watch('to_date', function (value) {
      try {
       $scope.to_date_obj = new Date(value);
       $scope.to_date_nice = getDateString($scope.to_date_obj);
       $scope.setData();
      } catch(e) {
        console.log(e)
      }
    });

    $scope.$watch('all_time', function(value) {
      $scope.setData();
    });

    $scope.openFromCalendar = function() {
      $element.find("#from_picker input").trigger("click")      
    }

    $scope.openToCalendar = function() {
      $element.find("#to_picker input").trigger("click")      
    }

    $scope.setData = function() {      
      $scope.dataLoaded = false

      var time_filter_url_string = ""      
      if (!$scope.all_time) {
        var from_unix = Math.floor($scope.from_date_obj.getTime()/1000)
        var to_unix = Math.floor($scope.to_date_obj.getTime()/1000)
        time_filter_url_string = from_unix + "/" + to_unix + "/"
      }

      var information = $scope.information_options[$attrs.information]
      var url = "http://localhost:8000/" + time_filter_url_string + information["url"]
      var result_type = information["type"]

      $scope.series = $scope.series.slice(0,0)
      if (result_type != 3) {
        $scope.series.push("Pakete")
      }

      $http.get(url).then(function success(response) {   
        $scope.no_data_available = Object.keys(response.data.values).length < 1
        
        $scope.data = $scope.data.slice(0,0)
        $scope.labels = $scope.labels.slice(0,0)
        
        if (result_type == 3) {
          for (var key in response.data.values) {
            if (response.data.values.hasOwnProperty(key)) {
              // Add all keynames in response (car, train, ...) as own series
              for (var keyname in Object.keys(response.data.values[key])) {
                if ($scope.series.indexOf(Object.keys(response.data.values[key])[keyname]) == -1) {
                  $scope.series.push(Object.keys(response.data.values[key])[keyname])                          
                }                
              }
            }
          }

          for (var i = 0; i < $scope.series.length; ++i) {
            var new_data_arr = []            
            for (var j = 0; j < Object.keys(response.data.values).length; ++j) {
              new_data_arr.push(0)
            }
            $scope.data.push(new_data_arr)
          }
        } else {
          // Type 1, 2
          $scope.data.push([])
        }

        var didx = 0
        for (var key in response.data.values) {
          if (response.data.values.hasOwnProperty(key)) {            
            if (result_type == 3) {
              // Add all keynames in response (car, train, ...) as own series
              for (var keyname in Object.keys(response.data.values[key])) {
                var keyname_str = Object.keys(response.data.values[key])[keyname]
                var series_idx = $scope.series.indexOf(keyname_str)                
                $scope.data[series_idx][didx] = response.data.values[key][keyname_str]
                
                if ($scope.labels.indexOf(key) == -1) {
                  $scope.labels.push(key)
                }
              }
            } else {
              // Type 1, 2
              let value = response.data.values[key]
              if (!information.filterfun || information.filterfun(key, value)) {
                $scope.data[0].push(value)
                $scope.labels.push(key)
              }
            }
          }
          didx++
        }

        $scope.dataLoaded = true
      }, function error() { 
        console.log("error");
      })
    }

    /*
    $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];

    $scope.options = {
      scales: {
        yAxes: [
          {
            id: 'y-axis-1',
            type: 'linear',
            display: true,
            position: 'left'
          },
          {
            id: 'y-axis-2',
            type: 'linear',
            display: true,
            position: 'right'
          }
        ]
      }
    }; */

    $scope.setData();
  }]);

  app.component("statistic", {
    "templateUrl": "templates/statistic.html",
    "bindings": {"name" : "@", "type" : "@"},    
    "controller": 'ChartController'
  });

})();