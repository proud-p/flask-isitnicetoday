


function getLocation() {

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
        // Hide loader if geolocation is not supported
     
    }
    }

function showPosition(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    
    fetch('/location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ latitude: latitude, longitude: longitude })
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
                  window.location.href = data.redirect;
              } else {
                  document.getElementById('weather-results').innerHTML = data.weather;
              }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('weather-results').innerHTML = 'Error fetching weather data';
        document.getElementById("loader").style.display = "none"; // Hide loader
                        document.getElementById("content").style.display = "block"; // Show content
    });
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}