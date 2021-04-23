function putvideo() {
  var path = document.getElementById("video").value;
  $.get("http://127.0.0.1:5000/getVideo", { path: path }, function (data) {
    console.log(data);
    document.getElementById("pp").innerHTML = data;
  });
}
