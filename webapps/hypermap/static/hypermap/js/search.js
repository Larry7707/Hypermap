var $j = jQuery.noConflict();
$j(document).ready(function ()
{
  $j("#search-form").on('submit', function(event) {
        event.preventDefault();
        // console.log(event.target);
        // var id = $j(event.target).data("post-id");
        // console.log("now commenting post"+ id);
        console.log("start_searching")
        var post_form = $j(event.target).serialize();
        $j.post("/hypermap/search-event", post_form)
        .done(function(data) {
          console.log("Search done.");
          // var list = $j("#comments_" + id);
          // getUpdates();
            var list = $j("#search-result");
            list.empty();
            list.append("<p> " + data.items.length + " results are found. </p><br>")
            for (var i = 0; i<data.items.length; i++) {
              list.append(data.items[i].html);
            }
        });
      });
});
