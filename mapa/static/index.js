var gdanskCoords = {lat: 54.354687, lng: 18.593562 }

var geocoder;
var map;

window.addEventListener('load', async function()
{
    map = await initMap(gdanskCoords);

    map.addListener('click', mapClicked);

    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((position) => {
              map.setCenter({lat: position.coords.latitude, lng: position.coords.longitude});
            });
        }

    addStop();
    addStop();

    await markAllBikeParking();
});