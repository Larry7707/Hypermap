var $j = jQuery.noConflict();

$j(document).ready(function () {
    Get_notes_num();
    window.setInterval(Get_notes_num, 5000);
});


function Get_notes_num() {
  $j.get("/hypermap/get-notes-num").done(function(data) {
    var note = $j("#note");
    if (data.num > 0) {
    note.html("NOTIFICATIONS <font size='4' \
                      color='red' face='Comic Sans MS'>" + 
                      data.num + "</font>");
    } else {
    note.html("NOTIFICATIONS <font size='4' \
                  color='black' face='Comic Sans MS'>(" + 
                  data.num + ")</font>");
    }
  });
}