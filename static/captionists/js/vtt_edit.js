var paused_by_focus = false;

var start_time_to_id = new Array();

function loadFile(url, timeout, callback) {
    var args = Array.prototype.slice.call(arguments, 3);
    var xhr = new XMLHttpRequest();
    xhr.ontimeout = function () {
        console.error("The request for " + url + " timed out.");
    };
    xhr.onload = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                callback.apply(xhr, args);
            } else {
                console.error(xhr.statusText);
            }
        }
    };
    xhr.open("GET", url, true);
    xhr.timeout = timeout;
    xhr.send(null);
}

function parse_and_attach(data) {
    var parser = new WebVTTParser();
    var cue_tree = parser.parse(data, 'metadata');

    var video = document.getElementById('video');
    var track = video.addTextTrack('captions', "English", "en");
    track.mode = "showing";

    var count = 0;
    for (var next_cue_key in cue_tree.cues) {
        var obj = cue_tree.cues[next_cue_key];
        // console.log(obj)
        var newCue = new VTTCue(obj.startTime, obj.endTime, obj.text);
        track.addCue(newCue);
        newCue.id = count;
        add_captions_to_table(count, obj.startTime, obj.endTime, obj.text);
        count++;
    }

    track.oncuechange = function(e){
      $(".cue-text").css('backgroundColor','');
      if(e.currentTarget.activeCues.length == 0) {
        return;
      }

      $('#cue_index_'+ e.currentTarget.activeCues[0].id).css('backgroundColor','#aaa')
    }
}

function pause_video() {
    document.getElementById('video').pause();
}


function update_cue(cue_index) {
    // console.log("updating cue index " + cue_index + " to " + document.getElementById('cue_index_' + cue_index).value) 
    video = document.getElementById('video');
    video.textTracks[0].cues[cue_index].text = document.getElementById('cue_index_' + cue_index).value;
}

function add_captions_to_table(count, start_time, end_time, text) {
    var table = document.getElementById("caption_table");
    var rowCount = table.rows.length;
    var row = table.insertRow(rowCount);

    start_time_to_id[start_time] = rowCount - 1;

    var cell0 = row.insertCell(0);
    cell0.innerHTML = "<div>" + start_time + "</div>"

    var cell1 = row.insertCell(1);
    cell1.innerHTML = "<div>" + end_time + "</div>"

    var cell2 = row.insertCell(2);
    cell2.innerHTML = "<textarea rows='3' class='cue-text' cols='50' id='cue_index_" + (rowCount - 1) + "' />"

    var cell3 = row.insertCell(3);
    cell3.innerHTML = "<img id='play_" + (rowCount - 1) + "' src='/static/captionists/icons/play.png'></img>"

    var input_box = document.getElementById('cue_index_' + (rowCount - 1))
    input_box.value = text
    input_box.addEventListener('change', function (e) {
        update_cue(rowCount - 1);
        if (paused_by_focus) {
            document.getElementById('video').currentTime = start_time;
            document.getElementById('video').play();
            paused_by_focus = false
        }
    });
    input_box.addEventListener('focus', function (e) {
        var video = document.getElementById('video')
        if (!video.paused) {
            video.pause();
            paused_by_focus = true;
        }

    });
    input_box.addEventListener('blur', function (e) {
        if (paused_by_focus) {
            // document.getElementById('video').currentTime = start_time;
            document.getElementById('video').play();
            paused_by_focus = false;
        }
    });


    var play_jump = document.getElementById('play_' + (rowCount - 1));
    play_jump.addEventListener('click', function (e) {
        document.getElementById('video').currentTime = start_time;
    });
}

function create_webvtt() {
    new_webvtt = "WEBVTT\n\n"
    var video = document.getElementById('video');
    // TODO get active track??
    for (var next_cue_id in video.textTracks[0].cues) {
        next_cue = video.textTracks[0].cues[next_cue_id]
        if (next_cue instanceof VTTCue) {
            new_webvtt += next_cue_id + "\n"
            start_time = new Date(next_cue.startTime * 1000).toISOString().slice(11, -1)
            end_time = new Date(next_cue.endTime * 1000).toISOString().slice(11, -1)
            new_webvtt += start_time + " --> " + end_time + "\n"
            new_webvtt += next_cue.text + "\n\n"
        }
    }
    // console.log(new_webvtt)

    var pathList = window.location.pathname.split('/');
    var post_url = "/subtitles/update/" + pathList[pathList.length - 2] + "/";
    console.log(post_url)

    $.post( post_url,
        {
            data: new_webvtt
        },
    function(data, status){
        console.log("Posted with status code: " + status);
    });
}

function cue_to_view() {
    // console.log("checking....")
    if (paused_by_focus) {
        // console.log("paused_by_focus")

        setTimeout(function(){cue_to_view()},3000);

        return;
    }

    var video = document.getElementById('video');
    if (video.textTracks.length < 1) {
        // console.log("no text track yet")

        setTimeout(function(){cue_to_view()},3000);

        return;
    }

    if (typeof video.textTracks[0].activeCues === "undefined") {
        // console.log("activeCues not defined yet")

        setTimeout(function(){cue_to_view()},3000);

        return;
    }
    
    if (video.textTracks[0].activeCues && video.textTracks[0].activeCues.length > 0) {
        var active_cue = video.textTracks[0].activeCues[0];
        // console.log("cue start time" + active_cue.startTime)
        var id_to_scroll = start_time_to_id[active_cue.startTime]

        var cue_element = document.getElementById('cue_index_' + id_to_scroll);
        // console.log("scrolling: " + id_to_scroll);
        if (cue_element && !video.paused) {
            // console.log("scrolling");
            cue_element.scrollIntoView();
        }
    }
    // console.log("seting alarm....")
    setTimeout(function(){cue_to_view()},3000);
}

function click(filename, action) {
            $.ajax({
                url: '/process/video/' + action + "/",
                data: {
                    'file_name': filename,
                    'language_code': "en-US"
                },
                type: 'POST',
                success: function () {
                    location.reload();
                },
                fail: function (error) {
                    alert(error);
                }
            });
        }