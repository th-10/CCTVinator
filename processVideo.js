const { PythonShell } = require("python-shell");
var path = require("path");

function processVideo() {
  //   var city = document.getElementById("city").value

  var options = {
    scriptPath: path.join(__dirname, "./"),
    args: [3],
  };

  let pyshell = new PythonShell("script.py", options);

  pyshell.on("message", function (message) {
    swal(message);
  });
  //   document.getElementById("city").value = "";
}
