async function initMap() {
const { Map } = await google.maps.importLibrary("maps");
var mapa = document.getElementById('map');
var map = new Map(mapa, {
  center: {lat: -34.397, lng: 150.644},
  zoom: 15
});
}

initMap();