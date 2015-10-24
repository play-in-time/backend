
playlists = [] // demo playlists


function updateInputBox() {
  var dropdownValue = $("#selectmode")[0].value;
  var inputBox = $("#inputbox")[0];
  var units = $("#units");
  
  if (dropdownValue == "for") {
    inputBox.placeholder = "42.5";
    units.text("hours");
  } else {
    inputBox.placeholder = "13:05";
    units.text("local time");
  }
}

$("#selectmode").change(function() {
  updateInputBox();
});

$(document).ready(function() {
  updateInputBox(); // Update the text input box to match the default

  // Fill out dropdown for playlist select:

});
