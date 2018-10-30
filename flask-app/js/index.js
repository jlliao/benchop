$(document).ready(function () {
  // initiate multi-select plugin
  $('#problems-selected').multiselect();

  // default parameters
  var parameters_1 = [100, 1.0, 0.03, 0.15];
  var parameters_2 = [100, 0.25, 0.1, 0.01];
  var titles = ['a) I', 'b) I', 'c) I', 'a) II', 'b) II', 'c) II']

  var id; // for which it will get a task id 

  createVariables(); // create variables for canvas

  // submit form
  $('#benchmark-button').click(function () {

    // define problems and parameters form input
    var problems = $('#problems-selected').val();
    var K1 = $('#K1').val(), T1 = $('#T1').val(), r1 = $('#r1').val(), sig1 = $('#sig1').val();
    var K2 = $('#K2').val(), T2 = $('#T2').val(), r2 = $('#r2').val(), sig2 = $('#sig2').val();

    // change parameters with form inputs
    if (K1 != "" && typeof K1 == 'number') { parameters_1[0] = K1 };
    if (T1 != "" && typeof T1 == 'number') { parameters_1[1] = T1 };
    if (r1 != "" && typeof r1 == 'number') { parameters_1[2] = r1 };
    if (sig1 != "" && typeof sig1 == 'number') { parameters_1[3] = sig1 };
    if (K2 != "" && typeof K2 == 'number') { parameters_2[0] = K2 };
    if (T2 != "" && typeof T2 == 'number') { parameters_2[1] = T2 };
    if (r2 != "" && typeof r2 == 'number') { parameters_2[2] = r2 };
    if (sig2 != "" && typeof sig2 == 'number') { parameters_2[3] = sig2 };

    // post data to run benchmark
    $.post("your-dockermachine-ip/runtask/", {
      problems: problems,
      parameters_1: parameters_1,
      parameters_2: parameters_2
    }, function (data) {
      id = data.id
    }, "json");

  });

  // check result
  $('#result-button').click(function () {

    $.get("your-dockermachine-ip/checktask/" + id, function (data) {
      var state = data.state;
      if (state == 'successful') {
        var results = JSON.parse(data.result);
        var canvas_id = 1;
        // draw bar chart for each result
        for (var i = 0; i < results.length; i++) {

          var d = results[i]
          var title = 'Problem 1 ' + titles[d['problem']];
          var x_labels;
          var time_list;
          var relerr_list;
          for (key in d) {
            x_labels.push(key);
            time_list.push(d[key][0]);
            relerr_list.push(d[key][1]);
          }
          window['time-' + canvas_id] = drawBarChart('time-bar-' + canvas_id, title, x_labels, time_list, 'time');
          window['relerr-' + canvas_id] = drawBarChart('relerr-bar-' + canvas_id, title, x_labels, time_list, 'relerr');

        }

      } else {
        $('#result').text("Result Not Yet Available")
      }
    }, "json");

  });

});

function drawBarChart(selector, title, x_labels, dataset, y_label) {
  return new Chart(selector, {
    // The type of chart we want to create
    type: 'bar',

    // The data for our dataset
    data: {
      labels: x_labels,
      datasets: [{
        label: title,
        backgroundColor: [
          color(window.chartColors.red).alpha(0.5).rgbString(),
          color(window.chartColors.blue).alpha(0.5).rgbString(),
          color(window.chartColors.green).alpha(0.5).rgbString()
        ],
        borderColor: [
          window.chartColors.red,
          window.chartColors.blue,
          window.chartColors.green
        ],
        data: dataset,
      }]
    },

    // Configuration options go here
    options: {
      scales: {
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: y_label
          }
        }]
      }
    }
  });
}
