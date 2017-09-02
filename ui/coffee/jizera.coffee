
latlng2str = (latlng) ->
    latstr = parseFloat(latlng.lat.toFixed(6))
    lngstr = parseFloat(latlng.lng.toFixed(6))
    "#{latstr}, #{lngstr}"

str2latlngs = (s) -> -1

dummy_handler = () -> 0

$(document).ready ->
    $('.js-off').hide()
    $('.js-on').show()
    return

run_geolocation = (handler = dummy_handler, handler_error = dummy_handler) ->
    if navigator.geolocation
        position_success = (position) ->
            geolatlng =
                lat: position.coords.latitude
                lng: position.coords.longitude
            handler geolatlng
        position_failure = (e) -> handler_error()
        navigator.geolocation.getCurrentPosition position_success, position_failure,
            timeout: 12 * 1000
            enableHighAccuracy: true
            maximumAge: 120 * 1000
    else
        handler_error()
