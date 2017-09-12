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
  // return run_geolocation(function(ll) {
  //   $('#fp-search-geoloc [name=lat]').val(ll.lat.toFixed(4));
  //   $('#fp-search-geoloc [name=lng]').val(ll.lng.toFixed(4));
  //   $('.geoloc-depend').show();
  //   return $('span.geoloc-depend').css('display', 'inline');
  // });
});
