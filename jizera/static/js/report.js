$(document).ready(function() {
  var update_toggles;
  update_toggles = function() {
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
  $('#localizeme').click(function() {
    alert('boomboom');
    return false;
  });
});
