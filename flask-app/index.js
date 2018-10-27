var resultElement = document.getElementById('result'),
  client = io('{{ notifier_url }}'),
  clientid = null;
client.on('register', function (id) {
  clientid = id;
});
client.on('notify', function (result) {
  resultElement.textContent = result;
  var dataset = [];
  var dataObj = JSON.parse(result);
  for (var i = 0; i < labelName.length; i++) {
    datapoint = dataObj[labelName[i]] / dataObj['total'];
    dataset.push(datapoint);
  }
  // Bar chart
  new Chart(document.getElementById("bar-chart"), {
    type: 'bar',
    data: {
      labels: labelName,
      datasets: [
        {
          label: "Relative frequency of pronouns (normalized)",
          backgroundColor: ["#3e95cd", "#ba7e5c", "#8e5ea2", "#3cba9f", "#7b4834", "#e8c3b9", "#c45850"],
          data: dataset
        }
      ]
    },
    options: {
      legend: { display: false },
      title: {
        display: true,
        text: 'Usage Frequency of Swedish Pronouns in Tweet'
      }
    }
  });
});
    document.querySelector('button').onclick = function () {
      var request = new XMLHttpRequest();
      request.open('POST', '/runtask', true);
      request.setRequestHeader(
        'Content-Type',
        'application/json');
      request.onload = function () {
        resultElement.textContent = request.responseText;
      };
      request.send(JSON.stringify({clientid: String(clientid), problems: }));
    };