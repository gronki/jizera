
$(document).ready ->
    run_geolocation (ll) ->
        $('#fp-search-geoloc [name=lat]').val ll.lat.toFixed(4)
        $('#fp-search-geoloc [name=lng]').val ll.lng.toFixed(4)
        $('.geoloc-depend').show()
        $('span.geoloc-depend').css 'display','inline'
