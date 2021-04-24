var imagelink;
async function readURL(input) {
  if (input.files && input.files[0]) {
    console.log(input.files[0].name);

    var reader = new FileReader();

    reader.onload = function (e) {
      $(".image-upload-wrap").hide();

      $(".file-upload-image").attr("src", e.target.result);
      $(".file-upload-content").show();

      $(".image-title").html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

    var $files = $(input).get(0).files;

    if ($files.length) {
      // Reject big files
      if ($files[0].size > $(this).data("max-size") * 1024) {
        console.log("Please select a smaller file");
        return false;
      }

      // var settings = {
      //   async: false,
      //   crossDomain: true,
      //   processData: false,
      //   contentType: false,
      //   type: "POST",
      //   url: apiUrl,
      //   headers: {
      //     Authorization: "Client-ID " + apiKey,
      //     Accept: "application/json"
      //   },
      //   mimeType: "multipart/form-data"
      // };

      var formData = new FormData();
      formData.append("image", $files[0]);
      // settings.data = formData;

      //loader On
      document.getElementById("loaderDiv").style.visibility = "visible";

      var path = "./../videos/" + input.files[0].name;
      await $.get(
        "http://127.0.0.1:5000/getVideo",
        { path: path },
        function (data) {
          console.log(data);
          data = JSON.stringify(data);
          localStorage.setItem("allData", data);
        }
      );

      //loader off
      document.getElementById("loaderDiv").style.visibility = "hidden";

      //btn next visible
      document.getElementById("hideBtn").style.visibility = "visible";
    }
  } else {
    removeUpload();
  }
  document.getElementById("addVideoBtnDisable").disabled = true;
  document.getElementById("removeVideoBtnDisable").disabled = true;
}

function removeUpload() {
  $(".file-upload-input").replaceWith($(".file-upload-input").clone());
  $(".file-upload-content").hide();
  $(".image-upload-wrap").show();
}
$(".image-upload-wrap").bind("dragover", function () {
  $(".image-upload-wrap").addClass("image-dropping");
});
$(".image-upload-wrap").bind("dragleave", function () {
  $(".image-upload-wrap").removeClass("image-dropping");
});
