async function initMap(coords)
{
    const { Map } = await google.maps.importLibrary("maps");
    const { Geometry } = await google.maps.importLibrary("geometry");
    const { Geocoding } = await google.maps.importLibrary("geocoding");
    geocoder = new google.maps.Geocoder();
    let map = new Map(document.getElementById('map'), {
      center: coords,
      zoom: 15,
      disableDefaultUI: true,
    });
    return map;
}

async function markAllBikeParking()
{
    var bikes = await getBikeParkings();
    bikes.forEach( (el) =>
    {
        markBike({lat: el.lat, lng: el.lng});
    });
}

function loadroad()
{
    fetch('/test', {
      method: 'GET',
    }).then(response => {
      if(response.ok){
          return response.json();
      }
        throw new Error('Request failed!');
    }, networkError => {
      console.log(networkError.message);
    }).then(jsonResponse => {
      console.log(jsonResponse);

    var p = google.maps.geometry.encoding.decodePath(jsonResponse['polyline']);

    const flightPath = new google.maps.Polyline({
    path: p,
    geodesic: true,
    strokeColor: "#FF0000",
    strokeOpacity: 1.0,
    strokeWeight: 2,
  });

    flightPath.setMap(map);

    });
}

function markBike(location) {
    var marker = new google.maps.Marker({
        position: location,
        icon: '/static/rsz_mevo.png',
        map: map
    });
}

function placeMarker(location) {
    return marker = new google.maps.Marker({
        position: location,
        map: map
    });
}

path = [];

function drawPath(path)
{
    console.log(path);
}