
var client_id = '29a0ec9178864f69b5e5e181811254ed';
var redirect_uri = 'http://playinti.me/callback.html';

var playlists = {};

// This is inactive for now
function doLogin() {
  var url = 'https://accounts.spotify.com/authorize?client_id=' + client_id +
            '&response_type=token' +
            '&scope=playlist-read-private%20playlist-modify%20playlist-modify-private' +
            '&redirect_uri=' + encodeURIComponent(redirect_uri);
  var w = window.open(url, 'asdf', 'WIDTH=400,HEIGHT=500');
}

function updateInputBox() {
  var dropdownValue = $("#selectmode")[0].value;
  var inputBox = $("#inputbox")[0];
  inputBox.value = "";
  var units = $("#units");
  
  if (dropdownValue == "for") {
    inputBox.placeholder = "42.5";
    units.text("minutes");
  } else {
    inputBox.placeholder = "13:05";
    units.text("local time");
  }
}

$("#selectmode").change(function() {
  updateInputBox();
});

// When the play button is clicked, submit request to the server
$("#playbutton").click(function() {
    var now = Math.floor(Date.now() / 1000); // Current time in seconds

    var inputBoxValue = $("#inputbox")[0].value;
    var mode = $("#selectmode")[0].value;
    var playlist = $("#selectPlaylist")[0].value;

    results = $("#results");
    loading = $("#loading");
    loading.hide();
    $("#total").remove();
    $("li").remove();
    if (inputBoxValue == "") {
      results.append("<p style=\"color:red\" class=\"err\">Please specify a time!</p>");
      results.show();
      return;
    }
    
    var duration = 0;
    var id = '0';
    if (mode == "for") {
      duration = parseInt(inputBoxValue)*60;
      id = playlists[playlist];

      
    } else {
      results.append("<p style=\"color:red\" class=\"err\">This mode isn't supported yet, sorry!</p>");
      results.show();
      return;
    }
    
    results.hide();
    $(".err").remove();

    var playMode = $("input[name=playmode]:checked").val();
    loading.show();
    if (playMode == "playlist") {
      var params = {'playlist_id': id, 'duration': duration};
      $.get("http://api.playinti.me/tracks_for_duration", params, function(res) {
          loading.hide();
          response = res.tracklist;

          var totalTime = 0;
          for (var i=0; i < response.length; i++) {
            var track = response[i].track;
            var name = track.name;
            var duration = (track.duration_ms / 1000)/60;
            totalTime += duration;

            resultList = $("#resultslist");
            tag = "<li>" + name + " (" + duration.toFixed(2) + " min)</li>";
            resultList.append(tag); 
          }

          results.append("<p id=\"total\">Total time: "+totalTime.toFixed(2)+" min</p>");

          console.log(res);
      });
    } else {
      var params = {'duration': duration};
      $.get("http://api.playinti.me/just_play", params, function(res) {
          loading.hide();
          response = res.tracklist;

          var totalTime = 0;
          for (var i=0; i < response.length; i++) {
            var track = response[i].track;
            var name = track.name;
            var duration = (track.duration_ms / 1000)/60;
            totalTime += duration;

            resultList = $("#resultslist");
            tag = "<li>" + name + " (" + duration.toFixed(2) + " min)</li>";
            resultList.append(tag); 
          }

          results.append("<p id=\"total\">Total time: "+totalTime.toFixed(2)+" min</p>");

          console.log(res);
      });
    }

    $("#results").show();
});

$(document).ready(function() {
  updateInputBox(); // Update the text input box to match the default

  // Fill out dropdown for playlist select:
  $.get('http://api.playinti.me/playlists', {}, function(res) {
      response = res.playlists;
      dropdown = $("#selectPlaylist");
     
      for (var i=0; i < response.length; i++) {
        var option = response[i].playlist_name;

        playlists[option] = response[i].playlist_id;
        dropdown.append("<option>"+option+"</option>");
      }
  });

  $("#results").hide();
});
