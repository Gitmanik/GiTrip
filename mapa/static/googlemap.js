async function initMap(coords)
{
    const { Map } = await google.maps.importLibrary("maps");
    const { Geometry } = await google.maps.importLibrary("geometry");

    var mapa = document.getElementById('map');
    let map = new Map(mapa, {
      center: coords,
      zoom: 15,
      disableDefaultUI: true,
    });
    return map;
}

var gdanskCoords = {lat: 54.354687, lng: 18.593562 }

var map;

window.addEventListener('load', async function()
{
    map = await initMap(gdanskCoords);

    map.addListener('click', function(event) {
        placeMarker(event.latLng);
    });

    // TO MUSI BYC OSTATNIE OK?
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((position) => {
          map.setCenter({lat: position.coords.latitude, lng: position.coords.longitude});
        });
    }
    await markAllBikes();
    loadroad();

});

async function markAllBikes()
{
    var bikes = await getBikes();
    bikes.forEach( (el) =>
    {
        markBike({lat: el.lat, lng: el.lng});
    });
}

async function getBikes()
{
    var response = await fetch('/allbikes', {
      method: 'GET',
    });
    if(response.ok){
        return await response.json();
    } else
    {
        return null;
    }
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
    var marker = new google.maps.Marker({
        position: location,
        map: map
    });
}
