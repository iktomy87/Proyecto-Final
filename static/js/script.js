document.addEventListener('DOMContentLoaded', function () {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            let lat = position.coords.latitude;
            let lon = position.coords.longitude;

            const url = `/get_weather/${lat}/${lon}/`;

            document.getElementById('spinner').style.display = 'block';
            document.getElementById('weather-icon').style.display = 'none';

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    const temp = data.main.temp.toFixed(1);
                    const icon = data.weather[0].icon;

                    // Hide spinner and show weather info
                    document.getElementById('spinner').style.display = 'none';
                    document.getElementById('weather-location').textContent = data.name;
                    document.getElementById('temperature').textContent = `\u00A0${temp}°C`;
                    document.getElementById('weather-icon').src = `http://openweathermap.org/img/wn/${icon}.png`;
                    document.getElementById('weather-icon').style.display = 'inline'; // Show the icon
                })
                .catch(error => {
                    console.error('Error fetching weather:', error);
                    // Hide spinner in case of error
                    document.getElementById('spinner').style.display = 'none';
                });
        });
    }

});

document.addEventListener('DOMContentLoaded', function() {
    const dateElement = document.getElementById('current-date');
    const today = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    dateElement.textContent = today.toLocaleDateString('es-ES', options); 
});