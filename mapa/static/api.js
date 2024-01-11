async function autocompleteRequest(inputValue) {

    var response = await fetch(base_url + '/api/autocomplete', {
      method: 'POST',
      body: JSON.stringify({ input: inputValue, lat: map.getCenter().lat(), lng: map.getCenter().lng() })
    });
    if(response.ok){
        var res = await response.json();
        console.log(res);
        return res;
    } else
    {
        return null;
    }
}

async function getBikes()
{
    var response = await fetch(base_url + '/api/allbikes', {
      method: 'GET',
    });
    if(response.ok){
        return await response.json();
    } else
    {
        return null;
    }
}

async function getBikeParkings()
{
    var response = await fetch(base_url + '/api/allbikeparkings', {
      method: 'GET',
    });
    if(response.ok){
        return await response.json();
    } else
    {
        return null;
    }
}