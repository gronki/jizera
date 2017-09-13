var dummy_handler, latlng2str, run_geolocation, str2latlngs;

function latlng2str(latlng) {
  var latstr, lngstr;
  latstr = parseFloat(latlng.lat.toFixed(6));
  lngstr = parseFloat(latlng.lng.toFixed(6));
  return latstr + ", " + lngstr;
};

str2latlngs = function(s) {
  return -1;
};

dummy_handler = function() {
  return 0;
};

$(document).ready(function() {
  $('.js-off').hide();
  $('.js-on').show();
});

function run_geolocation(handler, handler_error) {
  var position_failure, position_success;
  if (handler == null) {
    handler = dummy_handler;
  }
  if (handler_error == null) {
    handler_error = dummy_handler;
  }
  if (navigator.geolocation) {
    position_success = function(position) {
      var geolatlng;
      geolatlng = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      return handler(geolatlng);
    };
    position_failure = function(e) {
      return handler_error();
    };
    position_options = {
      timeout: 12 * 1000,
      enableHighAccuracy: true,
      maximumAge: 120 * 1000
    };
    return navigator.geolocation.getCurrentPosition(position_success, position_failure, position_options);
  } else {
    return handler_error();
  }
};
