$(document).ready ->
  update_toggles = ->
    tgt = $(this).attr('data-toggle')
    if $(this).prop('checked')
      $("##{tgt}").show()
    else
      $("##{tgt}").hide()
    return
  $('input[type="checkbox"][data-toggle]').each update_toggles
  $('input[type="checkbox"][data-toggle]').change update_toggles
  $('#localizeme').click ->
    alert 'boomboom'
    return false
  return
