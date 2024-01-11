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

function markBike(location) {
    var marker = new google.maps.Marker({
        position: location,
        icon: base_url + '/static/rsz_mevo.png',
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

function drawPath(p)
{
    console.log(p);
    path.forEach((e) => {
        e.setMap(null);
    });
    path = [];

    total_dist = 0;
    total_time = 0;

    p.forEach((e) => {

    console.log(e);

    total_dist += e.path.distance;
    total_time += e.path.duration;

    var line = google.maps.geometry.encoding.decodePath(e.path.polyline);

    color = "";

    switch (e.type){

        case "walk":
            color = "#00FF00";
            break;
        case 'mevo':
            color = "#FF0000";
            break;
        case 'tier':
            color = "#0000FF";
            break;

    }

    const marker = new google.maps.Polyline({
    path: line,
    geodesic: true,
    strokeColor: color,
    strokeOpacity: 1.0,
    strokeWeight: 2,
  });

    marker.setMap(map);
    path.push(marker);
    });

    document.getElementById('text').innerHTML = '<b>' + total_dist + 'm, ' + Math.floor(total_time / 60) + ' min</b>';

}