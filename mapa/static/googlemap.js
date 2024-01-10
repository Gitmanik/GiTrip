async function initMap(coords)
{
    const { Map } = await google.maps.importLibrary("maps");
    var mapa = document.getElementById('map');
    let map = new Map(mapa, {
      center: coords,
      zoom: 15,
      disableDefaultUI: true,
    });
    return map;
}

var gdanskCoords = {lat: 54.354687, lng: 18.593562 }

window.addEventListener('load', async function()
{
    var map = await initMap(gdanskCoords);

    // TO MUSI BYC OSTATNIE OK?
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((position) => {
          map.setCenter({lat: position.coords.latitude, lng: position.coords.longitude});
        });
    }

})