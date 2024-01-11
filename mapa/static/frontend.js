var markers = {};

function addStop()
{
    let referenceNode = document.getElementById('addStopButton').parentNode;
    let mainNode = referenceNode.parentNode;

    let stopDiv = document.createElement("div");
    stopDiv.classList.add("stop");

    let stopInput = document.createElement('input');
    stopInput.classList.add("boxInput");
    stopInput.id = "stop_input_" +  mainNode.childElementCount;
    stopInput.addEventListener(
        'keyup',
        async (e) => { await stopOnKeyUp(e); },
         false);
    stopDiv.appendChild(stopInput);

    let stopList = document.createElement("ul");
    stopList.classList.add('list');
    stopList.id = stopInput.id + "_list";
    stopDiv.appendChild(stopList);

    markers[stopInput.id] = null;

    mainNode.insertBefore(stopDiv, referenceNode);

    nameStops()

    if (document.querySelector(".inputContainer").querySelectorAll('.stop').length == 11)
    {
        document.getElementById('addStopButton').parentNode.remove();
    }
    return stopDiv;
}

function nameStops()
{
    let n = document.querySelector(".inputContainer").querySelectorAll('.stop');

    if (n.length == 0)
        return;

    var ctr = 0;
    n.forEach((e) => {
    let x = e.querySelector('input');
    if (x == null)
        return;

    if (ctr == 0)
        x.placeholder = "Skąd przybywasz?";
    else if (ctr == n.length - 2)
        x.placeholder = "Dokąd zmierzasz?";
    else
        x.placeholder = "Co cię zatrzymuje?";

    ctr++;
    });

}

async function stopOnKeyUp(e)
{
    let el = e.target;
    let val = el.value;

    setTimeout(async (el, val) => {
        console.log("Delayed for 1 second.");
        if (el.value != val)
        {
            console.log("nie ma co dzwonic");
            return;
        }
        console.log("mozna dzwonic");

        var autocomplete = await autocompleteRequest(val);

        if (autocomplete == null)
            return;

        let arr = [];
        autocomplete.forEach((x) => {
        arr.push("<b>" + x[0] + "</b></br><i>" + x[1] + "</i>")
        });

        populateList(el.id, el.id + "_list", arr, 'stopAutocompleteReady');
    }, "750", e.target, val);
}

function stopAutocompleteReady(el, va) {
    console.log(va);
    console.log(el);

    clearAllLists();
    const re = /<\/br><i>(.*)<\/i>/;

    if (re.test(va))
    {
        document.getElementById(el).value = va.match(re)[1];
        if (markers[el] != null)
        {
            markers[el].setMap(null);
            markers[el] = null;
        }

        geocoder.geocode( { 'address': va.match(re)[1]}, function(results, status) {
          console.log(status)
          if (status == 'OK') {
            markers[el] = placeMarker(results[0].geometry.location);
            checkAllFilled();
          } else {
            alert('Geocode was not successful for the following reason: ' + status);
            markers[el] = null;
          }
        });
    }
}


function mapClicked(event) {
    clearAllLists();

    let n = document.querySelector(".inputContainer").querySelectorAll('.stop');

    if (n.length == 0)
        return;

    var finished = false;
    n.forEach((e) => {
        let x = e.querySelector('input');
        if (x == null)
            return;

        if (finished)
        return;

        if (x.value == '')
        {
            if (markers[x.id] != null)
            {
                markers[x.id].setMap(null);
                markers[x.id] = null;
            }
            markers[x.id] = placeMarker(event.latLng);
            x.value = event.latLng;
            finished = true;
        }
    });

    if (!finished && n.length != 11)
    {
        let xx = addStop().querySelector('input');
        console.log(xx.id);
        markers[xx.id] = placeMarker(event.latLng);
        xx.value = event.latLng;
    }

    checkAllFilled();
}

function checkAllFilled() {
    let n = document.querySelector(".inputContainer").querySelectorAll('.stop');

    var empty = false;

    var list = [];

    n.forEach((e) => {
    console.log(e);
        let x = e.querySelector('input');
        if (x == null)
            return;

        if (x.value == '')
        {
            empty = true;
            return;
        }

        list.push(x.value);
    });
    if (empty)
        return;

    requestPath(list);
}

function requestPath(list)
{
    fetch(base_url + "/api/get_path", {
    method: "POST",
    body: JSON.stringify(list)
    }).then(response => {
      if(response.ok){
          return response.json();
      }
        throw new Error('Request failed!');
    }, networkError => {
      console.log(networkError.message);
    }).then(jsonResponse => {
        drawPath(jsonResponse);
    });
}