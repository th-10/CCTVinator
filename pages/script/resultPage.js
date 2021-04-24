videojs("my_video_1").ready(function () {
  // console.log(this.options()); //log all of the default videojs options

  // Store the video object
  var myPlayer = this,
    id = myPlayer.id();
  // Make up an aspect ratio
  var aspectRatio = 264 / 640;

  function resizeVideoJS() {
    var width = document.getElementById(id).parentElement.offsetWidth;
    myPlayer.width(width).height(width * aspectRatio);
  }

  // Initialize resizeVideoJS()
  resizeVideoJS();
  // Then on resize call resizeVideoJS()
  window.onresize = resizeVideoJS;
});

var data = localStorage.getItem("allData");
console.log(data);
var data2 = JSON.parse(data);
console.log(data2);
document.getElementById("filename").innerHTML = data2.filename + ".mp4";
document.getElementById("obj_detect").innerHTML = data2.total_objects;
document.getElementById("num_frames").innerHTML = data2.actual_frames;
document.getElementById("og_video_len").innerHTML = data2.actual_length;
document.getElementById("sm_video_len").innerHTML = "0:" + data2.new_time;
document.getElementById("reduction_len").innerHTML =
  Math.round(
    ((data2.actual_frames - data2.new_frames) / data2.actual_frames) * 100
  ) + "%";

// document.getElementById("summvideo").src =
//   "./summarized_videos/" + data2.filename + "_summary.mp4";
var player = videojs(document.getElementById("my_video_2"));
player.src({
  src: "./summarized_videos/" + data2.filename + "_summary.mp4",
  type: "video/mp4" /*video type*/,
});

player.play();

var player = videojs(document.getElementById("my_video_1"));
player.src({
  src: "./videos/" + data2.filename + ".mp4",
  type: "video/mp4" /*video type*/,
});

player.play();

for (i = 0; i < data2.timestamps.length; i++) {
  var list = `<li class="traffic-sales-content list-group-item">
                      <span class="traffic-sales-name">${
                        i + 1
                      } : Event Detected</span><span class="traffic-sales-amount">${
    data2.timestamps[i]
  }

                    </li>`;
  $("#events_list").append(list);
}
function openExplorer() {
  $.get("http://127.0.0.1:5000/openFile", function (data) {
    console.log(data);
  });
}
