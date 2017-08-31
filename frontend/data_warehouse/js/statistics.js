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

  let size_compare_weight = ['small', 'normal', 'big']

  let alphabetic_order = function (a, b) {
    return (a.key).localeCompare(b.key)
  }

  let hour_order = function (a, b) {
    return Number(a.key)-Number(b.key)
  }

  let day_order = function (a, b) {
    //dd.mm.yyyy
    let splita = a.key.split('.')
    let splitb = b.key.split('.')
    let dateA = new Date(splita[1]+"-"+splita[0]+"-"+splita[2])
    let dateB = new Date(splitb[1]+"-"+splitb[0]+"-"+splitb[2])
    return (dateA > dateB) - (dateA < dateB)
  }

  let ascending_values_numeric = function (a, b) {
    return a.value - b.value
  }



  app.controller('ChartController', ['$scope', '$http', '$attrs', '$element', function ($scope, $http, $attrs, $element) {
    $scope.labels = [];
    $scope.series = ['Pakete'];
    $scope.data   = [[]];    
    $scope.type_options = ["line", "pie", "bar"];
    $scope.type     = $scope.type_options[0];
    $scope.options  = { legend: { display: true } };    
    $scope.all_time = true

    $scope.colours = ['#72C02C', '#3498DB', '#717984', '#F1C40F'];

    $scope.dataLoaded = false

    $scope.from_date = new Date(0)
    $scope.from_date_obj = new Date(0)   
    $scope.from_date_nice = "-" 

    $scope.to_date = new Date()
    $scope.to_date_obj = new Date()
    $scope.to_date_nice = ""

    $scope.no_data_available = false
    $scope.error_occured = false

    $scope.information_options = {
        "sizes"         : {"url" : "size", "type" : 1,
        "sortfun" : function (a, b) {
            let index_a = size_compare_weight.indexOf(a.key)
            let index_b = size_compare_weight.indexOf(b.key)
            return index_a-index_b
        }, },
        "vehicles"      : {"url" : "location_vehicle_current", "type" : 1, "sortfun" : alphabetic_order,
        "filterfun" : function (text, zahl) {
            return text != "registert" && text != "delivery"
        }},
        "avg_delivery"  : {"url" : "average_delivery/day", "type" : 2, "sortfun" : day_order, 'unit' : 'Lieferzeit in Sekunden'},
        "location_day"  : {"url" : "location_vehicle_current/day", "type" : 3, "sortfun" : day_order},
        "location_hour" : {"url" : "location_vehicle_current/hour", "type" : 3, "sortfun" : hour_order},
        "avg_weight_day":{"url" : "average_weight/day", "type" : 2, "sortfun" : day_order, 'unit' : 'Gewicht in kg'},
        "registrations_day":{"url" : "registration/day", "type" : 2, "sortfun" : day_order},
        "registrations_hour":{"url" : "registration/hour", "type" : 2, "sortfun" : hour_order},
        "addresses"     : {"url" : "location_address_current", "type" : 1,
        "filterfun": function (text, zahl) {
            return text != "registert" && text != "delivery" && zahl >= 5
        }, "sortfun" : ascending_values_numeric},
        "city_send"     : {"url" : "sender_city", "type" : 1,
        "filterfun" : function (text, zahl) {
            return zahl > 100
        }, "sortfun" : ascending_values_numeric},
        "city_receive"     : {"url" : "receiver_city", "type" : 1,
        "filterfun" : function (text, zahl) {
            return zahl > 100
        }, "sortfun" : ascending_values_numeric}
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
        let unit = information.unit ? information.unit : "Pakete"
        $scope.series.push(unit)
      }

      $scope.error_occured = false
      $http.get(url).then(function success(response) {   
        $scope.no_data_available = Object.keys(response.data.values).length < 1
        
	//transform the data into array of key, value pairs
        var statistic_data = []
        for (var datakey in response.data.values) {
          statistic_data.push({key:datakey, value:response.data.values[datakey]})
        }

        //if available, sort the data
        if (information.sortfun) {
          statistic_data.sort(information.sortfun)
        }

        $scope.data = $scope.data.slice(0,0)
        $scope.labels = $scope.labels.slice(0,0)
        
        if (result_type == 3) {
          for(var i=0; i< statistic_data.length; ++i) {
            let datapoint = statistic_data[i]
            for(var value_index in Object.keys(datapoint.value)) {
              let subkey = Object.keys(datapoint.value)[value_index]
              if($scope.series.indexOf(subkey) == -1 && subkey != "registert") {
                $scope.series.push(subkey)
              }
            }
          }
          for (var i = 0; i< $scope.series.length; ++i) {
            var new_data_arr = new Array(statistic_data.length)
            new_data_arr.fill(0)
            $scope.data.push(new_data_arr)
          }
        } else {
          // Type 1, 2
          $scope.data.push([])
        }

        var didx = 0
        for (var i = 0; i<statistic_data.length; ++i) {
          let datapoint = statistic_data[i]
          if(result_type == 3) {
            // Add all keynames in response (car, train, ...) as own series
            let keys = Object.keys(datapoint.value)
            for (var subkey in keys) {
              var subkey_str = keys[subkey]
              var series_idx = $scope.series.indexOf(subkey_str)
              if (series_idx >= 0) {
                $scope.data[series_idx][didx] = datapoint.value[subkey_str]
                if($scope.labels.indexOf(datapoint.key) == -1) {
                  $scope.labels.push(datapoint.key)
                }
              }
            }
          }else{
            //Type 1,2
            if(!information.filterfun || information.filterfun(datapoint.key, datapoint.value)) {
              $scope.data[0].push(datapoint.value)
              $scope.labels.push(datapoint.key)
            }
          }
          didx++
        }

        $scope.dataLoaded = true
      }, function error() { 
        console.log("error");
        $scope.error_occured = true
        $scope.dataLoaded = true        
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
