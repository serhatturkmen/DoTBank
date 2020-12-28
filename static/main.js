$(document).ready(function(){
  $("#filterinput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filtertable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});