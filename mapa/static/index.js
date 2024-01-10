function sendRequest() {
    var inputValue = $("[name=start]").val();

    $.ajax({
        type: 'POST',
        url: '/nasze-api',
        data: { input: inputValue },
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.error('Error', error);
        }
    });
}

function sendRequestM() {
    var inputValue = $("[name=meta]").val();

    $.ajax({
        type: 'POST',
        url: '/nasze-api',
        data: { input: inputValue },
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.error('Error', error);
        }
    });
}

google.maps.event.addListener(map, 'click', function(event) {
    placeMarker(event.latLng);
});

function placeMarker(location) {
    var marker = new google.maps.Marker({
        position: location,
        map: map
    });
}
