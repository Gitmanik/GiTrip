async function autocompleteRequest(inputValue) {

    var response = await fetch('/api/autocomplete', {
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
    var response = await fetch('/api/allbikes', {
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
    var response = await fetch('/api/allbikeparkings', {
      method: 'GET',
    });
    if(response.ok){
        return await response.json();
    } else
    {
        return null;
    }
}