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

    input: inputValue, lat: map.getCenter().lat(), lng: map.getCenter().lng()

    map.addListener('click', function(event) {
        placeMarker(event.latLng);
    });

    // TO MUSI BYC OSTATNIE OK?
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((position) => {
          map.setCenter({lat: position.coords.latitude, lng: position.coords.longitude});
        });
    }

    loadroad();

})

function getBikes()
{
    fetch('/allbikes', {
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
      return null;
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

    })


}

function markBike(location) {
    var marker = new google.maps.Marker({
        position: location,
        icon: '/static/bike.jpg'
        map: map
    });
}

function placeMarker(location) {
    var marker = new google.maps.Marker({
        position: location,
        map: map
    });
}
