var $j = jQuery.noConflict();
// import {Get_notes_num} from 'hypermap_all'; 

function populateList() {
    $j.get("/hypermap/get-notes")
    .done(function(data) {
        var list = $j("#notes-list");
        for(var i = 0; i < data.notes.length; i++) {
            var note = $j(data.notes[i].html);

            // console.log(note);
            // note.data("note-id", data.notes[i].id);
            list.append(note);
            var div = $j("#note" + data.notes[i].id);
            div.data("note-id", data.notes[i].id)
            // console.log(div);
        }

        $j(".trend-box1").on("click", function(e) {
            // console.log($j(e.target).closest(".trend-box1"));

            var id = $j(e.target).closest(".trend-box1").data("note-id");
            $j.get("/hypermap/read-notes/" + id)
            .done(function(data){
                console.log("read");
                var note = $j("#content" + id);
                console.log(note);
                note.replaceWith(data.html);
                Get_notes_num();
            });
        });
    });
}

function getUpdates() {

}

$j(document).ready(function($){
    populateList();
    // window.setInterval(getUpdates, 5000);
});