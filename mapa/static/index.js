function sendRequest() {
    var inputValue = $("[name=start]").val();

    $.ajax({
        type: 'POST',
        url: '/nasze-api',
        data: { input: inputValue, lat: map.getCenter().lat(), lng: map.getCenter().lng() },
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
        data: { input: inputValue, lat: map.getCenter().lat(), lng: map.getCenter().lng() },
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.error('Error', error);
        }
    });
}