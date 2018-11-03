$(document).ready(function () {
  // initiate multi-select plugin
  $('#problems-selected').multiselect();

  // default parameters
  var problems = [];
  $('#problems-selected').on('change', function(){
    problems = $(this).val().map(Number);
  });

  var K1, T1, r1, sig1, K2, T2, r2, sig2;
  $('#K1, #T1, #r1, #sig1').on('change', function(){
    K1 = $('#K1').val(); T1 = $('#T1').val(); r1 = $('#r1').val(); sig1 = $('#sig1').val();
    K2 = $('#K2').val(); T2 = $('#T2').val(); r2 = $('#r2').val(); sig2 = $('#sig2').val();
  });

  var parameters_1 = [100, 1.0, 0.03, 0.15];
  var parameters_2 = [100, 0.25, 0.1, 0.01];
  var titles = ['a) I', 'b) I', 'c) I', 'a) II', 'b) II', 'c) II']

  var id; // for which it will get a task id 

  // submit form
  $('#benchmark-button').click(function () {

    // change parameters with form inputs
    if (K1 != null) { parameters_1[0] = K1 };
    if (T1 != null) { parameters_1[1] = T1 };
    if (r1 != null) { parameters_1[2] = r1 };
    if (sig1 != null) { parameters_1[3] = sig1 };
    if (K2 != null) { parameters_2[0] = K2 };
    if (T2 != null) { parameters_2[1] = T2 };
    if (r2 != null) { parameters_2[2] = r2 };
    if (sig2 != null) { parameters_2[3] = sig2 };

    parameters_1 = parameters_1.map(Number);
    parameters_2 = parameters_2.map(Number);

    // post data to run benchmark
    $.post("http://localhost:5000/runtask", 
    JSON.stringify({
      problems: problems,
      parameters1: parameters_1,
      parameters2: parameters_2
    }), function (data) {
      alert("Task id: " + data.id)
      id = data.id
    }, "json").fail(function(xhr, status, error) {
      // error handling
      alert("Task failed!")
      console.log(xhr.responseText);
    });

  });

  // check result
  $('#result-button').click(function () {

    $.get("http://localhost:5000/checktask/" + id, function (data) {
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
          x_labels = x_labels.map(stripString) // strip method name from strings of file name 
          window['time-' + canvas_id] = drawBarChart('time-bar-' + canvas_id, title, x_labels, time_list.map(Number), 'time');
          window['relerr-' + canvas_id] = drawBarChart('relerr-bar-' + canvas_id, title, x_labels, relerr_list.map(Number), 'relerr');

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
          'rgb(255, 99, 132, 0.5)', // red
          'rgb(54, 162, 235, 0.5)', // blue
          'rgb(75, 192, 192, 0.5)' // green
        ],
        borderColor: [
          'rgb(255, 99, 132)', // red
          'rgb(54, 162, 235)', // blue
          'rgb(75, 192, 192)' // green
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

// string handling for file names
function stripString(str) {
	var re = /^(.*)\_(\w+)\.m$/;
	var newString = str.replace(re, '$2');
	return(newString)
}