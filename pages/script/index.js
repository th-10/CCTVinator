function openCloudinary(){
    $.get("http://127.0.0.1:5000/openCloud", { link: "https://cloudinary.com/console/c-dccfe4d88c1407196d6d97c3938a6a/media_library/folders/7813ee3790f3a9f1ba18ea2f595164e0" }, function (data) {
      console.log(data);
    });
}
