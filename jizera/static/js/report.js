$(document).ready(function() {

  var update_toggles = function() {
    var tgt;
    tgt = $(this).attr('data-toggle');
    if ($(this).prop('checked')) {
      $("#" + tgt).show();
    } else {
      $("#" + tgt).hide();
    }
  };

  $('input[type="checkbox"][data-toggle]').each(update_toggles);
  $('input[type="checkbox"][data-toggle]').change(update_toggles);

  $('#localizeme').click(function(){
    run_geolocation(function(ll) {
      $('input[name=latitude]').val(ll.lat.toFixed(5));
      $('input[name=longitude]').val(ll.lng.toFixed(5));
    });
    return false;
  });

});
