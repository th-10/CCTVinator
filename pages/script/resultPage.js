// videojs("my_video_1").ready(function () {
//   // console.log(this.options()); //log all of the default videojs options

//   // Store the video object
//   var myPlayer = this,
//     id = myPlayer.id();
//   // Make up an aspect ratio
//   var aspectRatio = 264 / 640;

//   function resizeVideoJS() {
//     var width = document.getElementById(id).parentElement.offsetWidth;
//     myPlayer.width(width).height(width * aspectRatio);
//   }

//   // Initialize resizeVideoJS()
//   resizeVideoJS();
//   // Then on resize call resizeVideoJS()
//   window.onresize = resizeVideoJS;
// });

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
// cloud
var cl = new cloudinary.Cloudinary({ cloud_name: "demo", secure: true });

//
////////////////////////////put credentials

var fileSelect = document.getElementById("fileSelect"),
  fileElem = document.getElementById("fileElem"),
  urlSelect = document.getElementById("urlSelect");

var files = document.getElementById("myfile");
var f;
files.addEventListener("change", function (event) {
  console.log(event.target.files[0]);
  f = event.target.files[0];
});
function uploadclick() {
  document.getElementById("pro1").style.visibility = "visible";
  uploadFile(f);
}
// *********** Upload file to Cloudinary ******************** //
function uploadFile(file) {
  var url = `https://api.cloudinary.com/v1_1/${cloudName}/upload`;
  var xhr = new XMLHttpRequest();
  var fd = new FormData();
  xhr.open("POST", url, true);
  xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

  // Reset the upload progress bar
  document.getElementById("pro2").style.width = 0;

  // Update progress (can be used to show progress indicator)
  xhr.upload.addEventListener("progress", function (e) {
    var progress = Math.round((e.loaded * 100.0) / e.total);
    document.getElementById("pro2").style.width = progress + "%";

    console.log(`fileuploadprogress data.loaded: ${e.loaded},
  data.total: ${e.total}`);
  });

  xhr.onreadystatechange = function (e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
      // File uploaded successfully
      var response = JSON.parse(xhr.responseText);
      document.getElementById("pro1").style.visibility = "hidden";
      // https://res.cloudinary.com/cloudName/image/upload/v1483481128/public_id.jpg
      var url = response.secure_url;

      console.log(url);
      // Create a thumbnail of the uploaded image, with 150px width
      var tokens = url.split("/");
      tokens.splice(-2, 0, "w_150,c_scale");
      var img = new Image(); // HTML5 Constructor
      img.src = tokens.join("/");
      img.alt = response.public_id;
      // document.getElementById("gallery").appendChild(img);
    }
  };

  fd.append("upload_preset", unsignedUploadPreset);
  fd.append("tags", "browser_upload"); // Optional - add tag for image admin in Cloudinary
  fd.append("public_id", "CCTVinator/" + file.name);
  fd.append("file", file);
  xhr.send(fd);
}

// *********** Handle selected files ******************** //
// var handleFiles = function (files) {
//   for (var i = 0; i < files.length; i++) {
//     // uploadFile(files[i]); // call the function to upload the file
//     console.log(files);
//   }
// };
