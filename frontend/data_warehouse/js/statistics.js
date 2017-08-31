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

    $scope.dataLoaded = false

    $scope.from_date = new Date(0)
    $scope.to_date = new Date()

    $scope.from_date_obj = new Date(0)
    $scope.to_date_obj = new Date()

    $scope.no_data_available = false

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


    $scope.$watch('from_date', function (value) {
      try {
       $scope.from_date_obj = new Date(value);
      } catch(e) {
        console.log(e)
      }
    });

    $scope.$watch('to_date', function (value) {
      try {
       $scope.to_date_obj = new Date(value);
      } catch(e) {
        console.log(e)
      }
    });

    /*
    $scope.$watch('to_date', function (value) {
      try {
       $scope.to_date = new Date(value);
      } catch(e) {
        console.log(e)
      }
    });*/


    $scope.openFromCalendar = function() {
      $element.find("#from_picker input").trigger("click")
    }

    $scope.openToCalendar = function() {
      $element.find("#to_picker input").trigger("click")
    }

    $scope.setData = function() {
      $scope.dataLoaded = false

      var time_filter_url_string = ""
      console.log($scope.to_date)
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

      $http.get(url).then(function success(response) {
        console.log($element)

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


          // for (var key in response.data.values) {
          //   if (response.data.values.hasOwnProperty(key)) {
          //     // Add all keynames in response (car, train, ...) as own series
          //     for (var keyname in Object.keys(response.data.values[key])) {
          //       if ($scope.series.indexOf(Object.keys(response.data.values[key])[keyname]) == -1) {
          //         $scope.series.push(Object.keys(response.data.values[key])[keyname])
          //       }
          //     }
          //   }
          // }

          // for (var i = 0; i < $scope.series.length; ++i) {
          //   var new_data_arr = []
          //   for (var j = 0; j < Object.keys(response.data.values).length; ++j) {
          //     new_data_arr.push(0)
          //   }
          //   $scope.data.push(new_data_arr)
          // }
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


        // for (var key in response.data.values) {
        //   if (response.data.values.hasOwnProperty(key)) {
        //     if (result_type == 3) {
        //       // Add all keynames in response (car, train, ...) as own series
        //       for (var keyname in Object.keys(response.data.values[key])) {
        //         var keyname_str = Object.keys(response.data.values[key])[keyname]
        //         var series_idx = $scope.series.indexOf(keyname_str)
        //         $scope.data[series_idx][didx] = response.data.values[key][keyname_str]
        //
        //         if ($scope.labels.indexOf(key) == -1) {
        //           $scope.labels.push(key)
        //         }
        //       }
        //     } else {
        //       // Type 1, 2
        //       let value = response.data.values[key]
        //       if (!information.filterfun || information.filterfun(key, value)) {
        //         $scope.data[0].push(value)
        //         $scope.labels.push(key)
        //       }
        //     }
        //   }
        //   didx++
        // }

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

  /*

  app.controller('PieCtrl', ['$scope', '$http', function ($scope, $http) {
    $scope.labels = [];
    $scope.data = [];
    $scope.options = { legend: { display: true } };

    $scope.dataLoaded = false;

    $scope.setData = function() {
      $scope.dataLoaded = false

      $http.get("http://localhost:8000/getSizeDistribution").then(function success(response) {
        console.log(response.data)
        $scope.data = $scope.data.slice(0,0)
        $scope.labels = $scope.labels.slice(0,0)

        for (var key in response.data.values) {
          if (response.data.values.hasOwnProperty(key)) {
            $scope.data.push(response.data.values[key])
            $scope.labels.push(key)
          }
        }

        $scope.dataLoaded = true
      }, function error() {
        alert("error");
      })
    }

    $scope.setData()

  }]);


  app.controller('MenuCtrl', ['$scope', function ($scope) {
    $scope.isCollapsed = true;
    $scope.charts = ['Line', 'Bar', 'Doughnut', 'Pie', 'Polar Area', 'Radar', 'Horizontal Bar', 'Bubble', 'Base'];
  }]);

  app.controller('BarCtrl', ['$scope', function ($scope) {
    $scope.options = { legend: { display: true } };
    $scope.labels = ['2006', '2007', '2008', '2009', '2010', '2011', '2012'];
    $scope.series = ['Series A', 'Series B'];
    $scope.data = [
      [65, 59, 80, 81, 56, 55, 40],
      [28, 48, 40, 19, 86, 27, 90]
    ];
  }]);

  app.controller('DoughnutCtrl', ['$scope', '$timeout', function ($scope, $timeout) {
    $scope.labels = ['Download Sales', 'In-Store Sales', 'Mail-Order Sales'];
    $scope.data = [0, 0, 0];

    $timeout(function () {
      $scope.data = [350, 450, 100];
    }, 500);
  }]);



  app.controller('PolarAreaCtrl', ['$scope', function ($scope) {
    $scope.labels = ['Download Sales', 'In-Store Sales', 'Mail Sales', 'Telesales', 'Corporate Sales'];
    $scope.data = [300, 500, 100, 40, 120];
    $scope.options = { legend: { display: false } };
  }]);

  app.controller('BaseCtrl', ['$scope', function ($scope) {
    $scope.labels = ['Download Sales', 'Store Sales', 'Mail Sales', 'Telesales', 'Corporate Sales'];
    $scope.data = [300, 500, 100, 40, 120];
    $scope.type = 'polarArea';

    $scope.toggle = function () {
      $scope.type = $scope.type === 'polarArea' ?  'pie' : 'polarArea';
    };
  }]);

  app.controller('RadarCtrl', ['$scope', function ($scope) {
    $scope.labels = ['Eating', 'Drinking', 'Sleeping', 'Designing', 'Coding', 'Cycling', 'Running'];
    $scope.options = { legend: { display: false } };

    $scope.data = [
      [65, 59, 90, 81, 56, 55, 40],
      [28, 48, 40, 19, 96, 27, 100]
    ];

    $scope.onClick = function (points, evt) {
      console.log(points, evt);
    };
  }]);

  app.controller('StackedBarCtrl', ['$scope', function ($scope) {
    $scope.labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    $scope.type = 'StackedBar';
    $scope.series = ['2015', '2016'];
    $scope.options = {
      scales: {
        xAxes: [{
          stacked: true,
        }],
        yAxes: [{
          stacked: true
        }]
      }
    };

    $scope.data = [
      [65, 59, 90, 81, 56, 55, 40],
      [28, 48, 40, 19, 96, 27, 100]
    ];
  }]);

  app.controller('TabsCtrl', ['$scope', function ($scope) {
    $scope.labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    $scope.active = true;
    $scope.data = [
      [65, 59, 90, 81, 56, 55, 40],
      [28, 48, 40, 19, 96, 27, 100]
    ];
  }]);

  app.controller('MixedChartCtrl', ['$scope', function ($scope) {
    $scope.colors = ['#45b7cd', '#ff6384', '#ff8e72'];

    $scope.labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    $scope.data = [
      [65, -59, 80, 81, -56, 55, -40],
      [28, 48, -40, 19, 86, 27, 90]
    ];
    $scope.datasetOverride = [
      {
        label: 'Bar chart',
        borderWidth: 1,
        type: 'bar'
      },
      {
        label: 'Line chart',
        borderWidth: 3,
        hoverBackgroundColor: 'rgba(255,99,132,0.4)',
        hoverBorderColor: 'rgba(255,99,132,1)',
        type: 'line'
      }
    ];
  }]);

  app.controller('DataTablesCtrl', ['$scope', function ($scope) {
    $scope.labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    $scope.data = [
      [65, 59, 80, 81, 56, 55, 40],
      [28, 48, 40, 19, 86, 27, 90]
    ];
    $scope.colors = [
      { // grey
        backgroundColor: 'rgba(148,159,177,0.2)',
        pointBackgroundColor: 'rgba(148,159,177,1)',
        pointHoverBackgroundColor: 'rgba(148,159,177,1)',
        borderColor: 'rgba(148,159,177,1)',
        pointBorderColor: '#fff',
        pointHoverBorderColor: 'rgba(148,159,177,0.8)'
      },
      { // dark grey
        backgroundColor: 'rgba(77,83,96,0.2)',
        pointBackgroundColor: 'rgba(77,83,96,1)',
        pointHoverBackgroundColor: 'rgba(77,83,96,1)',
        borderColor: 'rgba(77,83,96,1)',
        pointBorderColor: '#fff',
        pointHoverBorderColor: 'rgba(77,83,96,0.8)'
      }
    ];
    $scope.options = { legend: { display: false } };
    $scope.randomize = function () {
      $scope.data = $scope.data.map(function (data) {
        return data.map(function (y) {
          y = y + Math.random() * 10 - 5;
          return parseInt(y < 0 ? 0 : y > 100 ? 100 : y);
        });
      });
    };
  }]);

  app.controller('BubbleCtrl', ['$scope', '$interval', function ($scope, $interval) {
    $scope.options = {
      scales: {
        xAxes: [{
          display: false,
          ticks: {
            max: 125,
            min: -125,
            stepSize: 10
          }
        }],
        yAxes: [{
          display: false,
          ticks: {
            max: 125,
            min: -125,
            stepSize: 10
          }
        }]
      }
    };

    createChart();
    $interval(createChart, 2000);

    function createChart () {
      $scope.data = [];
      for (var i = 0; i < 50; i++) {
        $scope.data.push([{
          x: randomScalingFactor(),
          y: randomScalingFactor(),
          r: randomRadius()
        }]);
      }
    }

    function randomScalingFactor () {
      return (Math.random() > 0.5 ? 1.0 : -1.0) * Math.round(Math.random() * 100);
    }

    function randomRadius () {
      return Math.abs(randomScalingFactor()) / 4;
    }
  }]);

  app.controller('TicksCtrl', ['$scope', '$interval', function ($scope, $interval) {
    var maximum = document.getElementById('container').clientWidth / 2 || 300;
    $scope.data = [[]];
    $scope.labels = [];
    $scope.options = {
      animation: {
        duration: 0
      },
      elements: {
        line: {
          borderWidth: 0.5
        },
        point: {
          radius: 0
        }
      },
      legend: {
        display: false
      },
      scales: {
        xAxes: [{
          display: false
        }],
        yAxes: [{
          display: false
        }],
        gridLines: {
          display: false
        }
      },
      tooltips: {
        enabled: false
      }
    };

    // Update the dataset at 25FPS for a smoothly-animating chart
    $interval(function () {
      getLiveChartData();
    }, 40);

    function getLiveChartData () {
      if ($scope.data[0].length) {
        $scope.labels = $scope.labels.slice(1);
        $scope.data[0] = $scope.data[0].slice(1);
      }

      while ($scope.data[0].length < maximum) {
        $scope.labels.push('');
        $scope.data[0].push(getRandomValue($scope.data[0]));
      }
    }
  }]);

  function getRandomValue (data) {
    var l = data.length, previous = l ? data[l - 1] : 50;
    var y = previous + Math.random() * 10 - 5;
    return y < 0 ? 0 : y > 100 ? 100 : y;
  }

  */
})();
